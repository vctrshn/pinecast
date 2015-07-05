import datetime
import time
from email.Utils import formatdate
from xml.sax.saxutils import escape, quoteattr

from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

import analytics.analyze as analyze
import analytics.log as analytics_log
from .models import Podcast, PodcastEpisode


def home(req):
    if not req.user.is_anonymous():
        return redirect('dashboard')

    if not req.POST:
        return render(req, 'login.html')

    try:
        user = User.objects.get(email=req.POST.get('email'))
        password = req.POST.get('password')
    except User.DoesNotExist:
        pass

    if (user and
        user.is_active and
        user.check_password(password)):
        login(req, authenticate(username=user.username, password=password))
        return redirect('dashboard')
    return render(req, 'login.html', {'error': 'Invalid credentials'})


def listen(req, episode_id):
    ep = get_object_or_404(PodcastEpisode, id=episode_id)
    if not analyze.is_bot(req) and req.method == 'GET':
        browser, device, os = analyze.get_device_type(req)
        analytics_log.write('listen', {
            'podcast': unicode(ep.podcast.id),
            'episode': unicode(ep.id),
            'source': 'rss' if req.GET.get('rss') else 'embed' if req.GET.get('embed') else 'direct',
            'profile': {
                'ip': analyze.get_request_ip(req),
                'ua': req.META.get('HTTP_USER_AGENT'),
                'browser': browser,
                'device': device,
                'os': os,
            },
        })

    return redirect(ep.audio_url)


def feed(req, podcast_slug):
    pod = get_object_or_404(Podcast, slug=podcast_slug)

    items = []
    for ep in pod.podcastepisode_set.filter(publish__lt=datetime.datetime.now()):
        duration = datetime.timedelta(seconds=ep.duration)
        items.append('\n'.join([
            '<item>',
                '<title>%s</title>' % escape(ep.title),
                '<description><![CDATA[%s]]></description>' % ep.description,
                '<link>/listen/%s?rss=true</link>' % escape(str(ep.id)),
                '<guid isPermaLink="false">http://almostbetter.net/guid/%s</guid>' % escape(str(ep.id)),
                '<pubDate>%s</pubDate>' % formatdate(time.mktime(ep.publish.timetuple())),
                '<itunes:author>%s</itunes:author>' % escape(pod.author_name),
                '<itunes:subtitle>%s</itunes:subtitle>' % escape(ep.subtitle),
                '<itunes:summary><![CDATA[%s]]></itunes:summary>' % ep.description,
                '<itunes:image href=%s />' % quoteattr(ep.image_url),
                '<itunes:duration>%s</itunes:duration>' % escape(str(duration)),
                '<enclosure url="/listen/%s?rss=true" length=%s type=%s />' % (
                    quoteattr(str(ep.id))[1:-1], quoteattr(str(ep.audio_size)), quoteattr(ep.audio_type)),
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
            '<itunes:image href=%s />' % quoteattr(pod.cover_image),
            '\n'.join(items),
        '</channel>',
        '</rss>',
    ]

    if not analyze.is_bot(req):
        browser, device, os = analyze.get_device_type(req)
        analytics_log.write('subscribe', {
            'id': analyze.get_request_hash(req),
            'podcast': unicode(pod.id),
            'profile': {
                'ip': analyze.get_request_ip(req),
                'ua': req.META.get('HTTP_USER_AGENT'),
                'browser': browser,
                'device': device,
                'os': os,
            },
        })

    return HttpResponse('\n'.join(content), content_type='application/rss+xml')
