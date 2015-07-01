import base64
import datetime
import hashlib
import hmac
import json
import time
import urllib
import uuid
from email.Utils import formatdate
from xml.sax.saxutils import escape, quoteattr

from django.conf import settings
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

import analytics.analyze as analyze
import analytics.log as analytics_log
from .models import Podcast, PodcastEpisode


def _pmrender(req, template, data=None):
    data = data or {}
    if not req.user.is_anonymous():
        data.setdefault('user', req.user)
        data.setdefault('podcasts', req.user.podcast_set.all())
        user_avatar = hashlib.md5(req.user.email).hexdigest()
        data.setdefault('user_avatar', 'http://www.gravatar.com/avatar/%s?s=40' % user_avatar)
    return render(req, template, data)


def home(req):
    if not req.user.is_anonymous():
        return redirect('dashboard')

    if not req.POST:
        return _pmrender(req, 'login.html')

    try:
        user = User.objects.get(email=req.POST.get('email'))
        password = req.POST.get('password') 
        if (user.is_active and
            user.check_password(password)):
            login(req, authenticate(username=user.username, password=password))
            return redirect('dashboard')
    except User.DoesNotExist:
        pass
    return _pmrender(req, 'login.html', {'error': 'Invalid credentials'})


@login_required
def dashboard(req):
    return _pmrender(req, 'dashboard.html')


@login_required
def podcast_dashboard(req, podcast_slug):
    pod = get_object_or_404(Podcast, slug=podcast_slug, owner=req.user)
    data = {
        'podcast': pod,
        'episodes': pod.podcastepisode_set.order_by('-publish'),
    }
    return _pmrender(req, 'dashboard/podcast.html', data)


@login_required
def podcast_new_ep(req, podcast_slug):
    pod = get_object_or_404(Podcast, slug=podcast_slug, owner=req.user)

    if not req.POST:
        return _pmrender(req, 'dashboard/new_episode.html', {'podcast': pod})

    ep = PodcastEpisode(
        podcast=pod,
        title=req.POST.get('title'),
        subtitle=req.POST.get('subtitle'),
        publish=datetime.datetime.strptime(req.POST.get('publish'), '%Y-%m-%dT%H:%M'), # 2015-07-09T12:00
        description=req.POST.get('description'),
        duration=int(req.POST.get('duration-hours')) * 3600 + int(req.POST.get('duration-minutes')) * 60 + int(req.POST.get('duration-seconds')),

        audio_url=req.POST.get('audio-url'),
        audio_size=int(req.POST.get('audio-url-size')),
        audio_type=req.POST.get('audio-url-type'),

        image_url=req.POST.get('iamge-url'),

        copyright=req.POST.get('copyright'),
        license=req.POST.get('license')
    )
    ep.save()
    return redirect('/dashboard/podcast/%s' % pod.slug)


@login_required
def get_upload_url(req, podcast_slug, type):
    if type not in ['audio', 'image']:
        return Http404()

    pod = get_object_or_404(Podcast, slug=podcast_slug, owner=req.user)
    extension = 'mp3' if type == 'audio' else 'jpg'
    basepath = 'podcasts/%s/%s/' % (pod.id, type)
    path = '%s%s.%s' % (basepath, str(uuid.uuid4()), extension)

    mime_type = req.GET.get('type')

    expires = int(time.time() + 60 * 60 * 24)
    amz_headers = 'x-amz-acl:public-read'

    string_to_sign = "PUT\n\n%s\n%d\n%s\n/%s/%s" % (mime_type, expires, amz_headers, settings.S3_BUCKET, path)
    signature = base64.encodestring(hmac.new(settings.S3_SECRET_KEY.encode(), string_to_sign.encode('utf8'), hashlib.sha1).digest())
    signature = urllib.quote_plus(signature.strip())

    destination_url = 'http://%s.s3.amazonaws.com/%s' % (settings.S3_BUCKET, path)
    data = {
        'url': '%s?AWSAccessKeyId=%s&Expires=%s&Signature=%s' % (destination_url, settings.S3_ACCESS_ID, expires, signature),
        'headers': {
            'x-amz-acl': 'public-read',
        },
        'destination_url': destination_url,
    }

    return HttpResponse(json.dumps(data), content_type='application/json')


def listen(req, episode_id):
    ep = get_object_or_404(PodcastEpisode, id=episode_id)
    if not analyze.is_bot(req):
        browser, device, os = analyze.get_device_type(req)
        write('listen', {
            'podcast': ep.podcast.id,
            'episode': ep.id,
            'profile': {
                'browser': browser,
                'device': device,
                'os': os,
            },
        })

    return redirect(ep.audio_url)


def feed(req, podcast_slug):
    pod = get_object_or_404(Podcast, slug=podcast_slug)

    items = []
    for ep in pod.podcastepisode_set.filter(publish__lt=datetime.now()):
        duration = datetime.timedelta(seconds=ep.duration)
        items.append('\n'.join([
            '<item>',
                '<title>%s</title>' % escape(ep.title),
                '<description><![CDATA[%s]]></description>' % ep.description,
                '<link>/listen/%s</link>' % escape(ep.id),
                '<guid isPermaLink="false">http://almostbetter.net/guid/%s</guid>' % escape(str(ep.id)),
                '<pubDate>%s</pubDate>' % formatdate(time.mktime(ep.publish.timetuple())),
                '<itunes:author>%s</itunes:author>' % escape(pod.author_name),
                '<itunes:subtitle>%s</itunes:subtitle>' % escape(ep.subtitle),
                '<itunes:summary><![CDATA[%s]]></itunes:summary>' % ep.description,
                '<itunes:image href="%s" />' % quoteattr(ep.image_url),
                '<itunes:duration>%s</itunes:duration>' % escape(str(duration)),
                '<enclosure url="/listen/%s" length="%s" type="%s" />' % (
                    quoteattr(ep.id), quoteattr(ep.audio_size), quoteattr(ep.audio_type)),
            '</item>',
        ]))

    content = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<rss xmlns:atom="http://www.w3.org/2005/Atom" xmlns:itunes="http://www.itunes.com/dtds/podcast-1.0.dtd" version="2.0">',
        '<channel>',
            '<title>%s</title>' % escape(pod.name),
            '<link>%s</link>' % escape(pod.homepage),
            '<language>%s</language>' % escape(pod.language),
            '<copyright>%s</copyright>' % escape(pod.copyright),
            '<itunes:subtitle>%s</itunes:subtitle>' % escape(pod.subtitle),
            '<itunes:author>%s</itunes:author>' % escape(pod.author_name),
            '<itunes:summary><![CDATA[%s]]></itunes:summary>' % pod.description,
            '<description><![CDATA[%s]]></description>' % pod.description,
            '<itunes:owner>',
                '<itunes:name>%s</itunes:name>' % escape(pod.author_name),
                '<itunes:email>%s</itunes:email>' % escape(pod.owner.email),
            '</itunes:owner>',
            '<itunes:explicit>%s</itunes:explicit>' % ('yes' if pod.is_explicit else 'no'),
            '<itunes:image href="%s" />' % quoteattr(pod.cover_image),
            '\n'.join(items),
        '</channel>',
        '</rss>',
    ]

    if not analyze.is_bot(req):
        browser, device, os = analyze.get_device_type(req)
        write('subscribe', {
            'podcast': ep.podcast.id,
            'profile': {
                'browser': browser,
                'device': device,
                'os': os,
            },
        })

    return HttpResponse('\n'.join(content), content_type='application/rss+xml')
