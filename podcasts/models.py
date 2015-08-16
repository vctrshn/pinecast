import datetime
import re
import uuid

import requests
from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext, ugettext_lazy

import accounts.payment_plans as payment_plans
from accounts.models import Network, UserSettings
from pinecast.helpers import cached_method


class Podcast(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    slug = models.SlugField(unique=True)

    name = models.CharField(max_length=256)
    subtitle = models.CharField(max_length=512, default='', blank=True)

    created = models.DateTimeField(auto_now=True)
    cover_image = models.URLField()
    description = models.TextField()
    is_explicit = models.BooleanField()
    homepage = models.URLField()

    language = models.CharField(max_length=16)
    copyright = models.CharField(max_length=1024, blank=True)
    author_name = models.CharField(max_length=1024)

    owner = models.ForeignKey(User)

    rss_redirect = models.URLField(null=True, blank=True)
    stats_base_listens = models.PositiveIntegerField(default=0)

    networks = models.ManyToManyField(Network)

    @cached_method
    def get_asset_bucket(self):
        use_premium_cdn = UserSettings.get_from_user(self.owner).use_cdn()
        return settings.S3_PREMIUM_BUCKET if use_premium_cdn else settings.S3_BUCKET

    @cached_method
    def get_category_list(self):
        return ','.join(x.category for x in self.podcastcategory_set.all())

    def set_category_list(self, cat_str):
        existing = set(x.category for x in self.podcastcategory_set.all())
        new = set(cat_str.split(','))

        added = new - existing
        removed = existing - new

        for a in added:
            n = PodcastCategory(podcast=self, category=a)
            n.save()

        for r in removed:
            o = PodcastCategory.objects.get(podcast=self, category=r)
            o.delete()

    @cached_method
    def is_still_importing(self):
        return bool(
            self.assetimportrequest_set.filter(failed=False, resolved=False).count())

    @cached_method
    def get_episodes(self):
        episodes = self.podcastepisode_set.filter(
            publish__lt=datetime.datetime.now(),
            awaiting_import=False).order_by('-publish')
        if UserSettings.get_from_user(self.owner).plan == payment_plans.PLAN_DEMO:
            episodes = episodes[:10]
        return episodes

    @cached_method
    def get_unpublished_count(self):
        return self.podcastepisode_set.filter(publish__gt=datetime.datetime.now()).count()

    @cached_method
    def get_most_recent_publish_date(self):
        if not self.podcastepisode_set.count():
            return None
        return self.podcastepisode_set.filter(publish__gt=datetime.datetime.now()).count()

    def __unicode__(self):
        return self.name


class PodcastEpisode(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    podcast = models.ForeignKey(Podcast)
    title = models.CharField(max_length=1024)
    subtitle = models.CharField(max_length=1024, default='')
    created = models.DateTimeField(auto_now=True)
    publish = models.DateTimeField()
    description = models.TextField(default='')
    duration = models.PositiveIntegerField(help_text=ugettext_lazy('Audio duration in seconds'))

    audio_url = models.URLField()
    audio_size = models.PositiveIntegerField(default=0)
    audio_type = models.CharField(max_length=64)

    image_url = models.URLField()

    copyright = models.CharField(max_length=1024)
    license = models.CharField(max_length=1024, blank=True)

    awaiting_import = models.BooleanField(default=False)

    @cached_method
    def formatted_duration(self):
        seconds = self.duration
        return '%02d:%02d:%02d' % (seconds // 3600, seconds % 3600 // 60, seconds % 60)

    @cached_method
    def is_published(self):
        return not self.awaiting_import and self.publish <= datetime.datetime.now()

    def __unicode__(self):
        return '%s - %s' % (self.title, self.subtitle)


CATEGORIES = set([
    'Arts',
    'Arts/Design',
    'Arts/Fashion & Beauty',
    'Arts/Food',
    'Arts/Literature',
    'Arts/Performing Arts',
    'Arts/Spoken Word',
    'Arts/Visual Arts',
    'Business',
    'Business/Business News',
    'Business/Careers',
    'Business/Investing',
    'Business/Management & Marketing',
    'Business/Shopping',
    'Comedy',
    'Education',
    'Education/Educational Technology',
    'Education/Higher Education',
    'Education/K-12',
    'Education/Language Courses',
    'Education/Training',
    'Games & Hobbies',
    'Games & Hobbies/Automotive',
    'Games & Hobbies/Aviation',
    'Games & Hobbies/Hobbies',
    'Games & Hobbies/Other Games',
    'Games & Hobbies/Video Games',
    'Government & Organizations',
    'Government & Organizations/Local',
    'Government & Organizations/National',
    'Government & Organizations/Non-Profit',
    'Government & Organizations/Regional',
    'Health',
    'Health/Alternative Health',
    'Health/Fitness & Nutrition',
    'Health/Self-Help',
    'Health/Sexuality',
    'Health/Kids & Family',
    'Music',
    'Music/Alternative',
    'Music/Blues',
    'Music/Country',
    'Music/Easy Listening',
    'Music/Electronic',
    'Music/Electronic/Acid House',
    'Music/Electronic/Ambient',
    'Music/Electronic/Big Beat',
    'Music/Electronic/Breakbeat',
    'Music/Electronic/Disco',
    'Music/Electronic/Downtempo',
    'Music/Electronic/Drum \'n\' Bass',
    'Music/Electronic/Garage',
    'Music/Electronic/Hard House',
    'Music/Electronic/House',
    'Music/Electronic/IDM',
    'Music/Electronic/Jungle',
    'Music/Electronic/Progressive',
    'Music/Electronic/Techno',
    'Music/Electronic/Trance',
    'Music/Electronic/Tribal',
    'Music/Electronic/Trip Hop',
    'Music/Folk',
    'Music/Freeform',
    'Music/Hip-Hop & Rap',
    'Music/Inspirational',
    'Music/Jazz',
    'Music/Latin',
    'Music/Metal',
    'Music/New Age',
    'Music/Oldies',
    'Music/Pop',
    'Music/R&B & Urban',
    'Music/Reggae',
    'Music/Rock',
    'Music/Seasonal & Holiday',
    'Music/Soundtracks',
    'Music/World',
    'News & Politics',
    'News & Politics/Conservative (Right)',
    'News & Politics/Liberal (Left)',
    'Religion & Spirituality',
    'Religion & Spirituality/Buddhism',
    'Religion & Spirituality/Christianity',
    'Religion & Spirituality/Hinduism',
    'Religion & Spirituality/Islam',
    'Religion & Spirituality/Judaism',
    'Religion & Spirituality/Other',
    'Religion & Spirituality/Spirituality',
    'Science & Medicine',
    'Science & Medicine/Medicine',
    'Science & Medicine/Natural Sciences',
    'Science & Medicine/Social Sciences',
    'Society & Culture',
    'Society & Culture/Gay & Lesbian',
    'Society & Culture/History',
    'Society & Culture/Personal Journals',
    'Society & Culture/Philosophy',
    'Society & Culture/Places & Travel',
    'Sports & Recreation',
    'Sports & Recreation/Amateur',
    'Sports & Recreation/College & High School',
    'Sports & Recreation/Outdoor',
    'Sports & Recreation/Professional',
    'TV & Film',
    'Technology',
    'Technology/Gadgets',
    'Technology/IT News',
    'Technology/Podcasting',
    'Technology/Software How-To',
])

class PodcastCategory(models.Model):
    category = models.CharField(max_length=128,
                                choices=[(x, x) for x in CATEGORIES])
    podcast = models.ForeignKey(Podcast)

    def __unicode__(self):
        return '%s: %s' % (self.podcast.name, self.category)


class PodcastReviewAssociation(models.Model):
    SERVICE_ITUNES = 'ITUNES'
    SERVICE_STITCHER = 'STITCHER'
    SERVICES = (
        (SERVICE_ITUNES, 'iTunes'),
        (SERVICE_STITCHER, 'Stitcher Radio'),
    )
    SERVICES_SET = set(x for x, y in SERVICES)
    SERVICES_MAP = {x: y for x, y in SERVICES}

    EXAMPLE_URLS = {
        SERVICE_ITUNES: 'https://itunes.apple.com/us/podcast/this-american-life/id201671138',
        SERVICE_STITCHER: 'http://www.stitcher.com/podcast/this-american-life',
    }

    podcast = models.ForeignKey(Podcast)  # Not one-to-one because you can have multiple services
    service = models.CharField(choices=SERVICES, max_length=16)    
    payload = models.CharField(max_length=256)    

    def __unicode__(self):
        return '%s: %s' % (self.podcast.name, self.service)

    @classmethod
    def create_for_service(cls, service, **kwargs):
        kwargs['service'] = service
        if service == SERVICE_STITCHER:
            return cls.create_service_stitcher(**kwargs)
        elif service == SERVICE_ITUNES:
            return cls.create_service_itunes(**kwargs)
        else:
            raise Exception('Unknown service')

    @classmethod
    def create_service_stitcher(cls, **kwargs):
        stitcher_page = requests.get(kwargs['url'], timeout=5)
        result = re.search(r'productId:\s+"(\w+)"', stitcher_page.text)
        if not result:
            raise Exception(ugettext('Could not find podcast ID'))

        return cls(payload=result.group(1), **kwargs)

    @classmethod
    def create_service_itunes(cls, **kwargs):
        page = requests.get(kwargs['url'], timeout=5, headers={'user-agent': 'iTunes/9.1.1'})
        result = re.search(r'<string>\s*(https://itunes\.apple\.com/.*)\s*</string>', page.text)
        if not result:
            raise Exception(ugettext('Could not find podcast ID'))

        return cls(payload=result.group(1), **kwargs)
