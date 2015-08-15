import gfm
from django.contrib.syndication.views import Feed
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from . import models
from pinecast.helpers import reverse


SITE_EPISODES_PER_PAGE = 5


def _srender(req, site, template, data=None):
    data = data or {}
    data.setdefault('site', site)
    return render(req, 'sites/%s/%s' % (site.theme, template), data)


def site_home(req, site_slug):
    site = get_object_or_404(models.Site, slug=site_slug)
    episodes = site.podcast.podcastepisode_set.all().order_by('-publish')
    paginator = Paginator(episodes, SITE_EPISODES_PER_PAGE)
    try:
        pager = paginator.page(req.GET.get('page'))
    except PageNotAnInteger:
        pager = paginator.page(1)
    except EmptyPage:
        return redirect('site_home', site_slug=site_slug)
    return _srender(req, site, 'home.html', {'pager': pager})


def site_blog(req, site_slug):
    site = get_object_or_404(models.Site, slug=site_slug)
    posts = site.siteblogpost_set.all().order_by('-publish')
    paginator = Paginator(posts, 5)
    try:
        pager = paginator.page(req.GET.get('page'))
    except PageNotAnInteger:
        pager = paginator.page(1)
    except EmptyPage:
        return redirect('site_home', site_slug=site_slug)
    return _srender(req, site, 'blog.html', {'pager': pager})

def site_post(req, site_slug, post_slug):
    site = get_object_or_404(models.Site, slug=site_slug)
    post = get_object_or_404(models.SiteBlogPost, site=site, slug=post_slug)
    return _srender(req, site, 'post.html', {'post': post})


class BlogRSS(Feed):

    def get_object(self, req, site_slug):
        return get_object_or_404(models.Site, slug=site_slug)

    def title(self, obj):
        return obj.podcast.name

    def link(self, obj):
        return reverse('site_home', site_slug=obj.slug)

    def description(self, obj):
        return obj.podcast.description

    def items(self, obj):
        return obj.siteblogpost_set.order_by('-publish')

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return gfm.markdown(item.body)

    def item_link(self, item):
        return reverse('site_post', site_slug=item.site.slug, post_slug=item.slug)

    item_guid_is_permalink = True

    def item_author_name(self, item):
        return item.site.podcast.author_name

    def item_pubdate(self, item):
        return item.publish

    def item_copyright(self, item):
        return item.site.podcast.copyright


def sitemap(req, site_slug):
    site = get_object_or_404(models.Site, slug=site_slug)

    output = '''<?xml version="1.0" encoding="UTF-8"?>
    <urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
    '''

    pages = site.podcast.podcastepisode_set.all().count()
    for i in xrange(pages):
        output += '''
        <url>
            <loc>{url}</loc>
            <changefreq>weekly</changefreq>
        </url>
        '''.format(url='%s?page=%d' % (reverse('site_home', site_slug=site_slug), i + 1))

    output += '''
    <url><loc>{url}</loc></url>
    '''.format(url=reverse('site_blog', site_slug=site_slug))

    for post in site.siteblogpost_set.all():
        output += '''
        <url><loc>{url}</loc></url>
        '''.format(url=reverse('site_post', site_slug=site_slug, post_slug=post.slug))


    output += '</urlset>'

    return HttpResponse(output, content_type='application/xml')
