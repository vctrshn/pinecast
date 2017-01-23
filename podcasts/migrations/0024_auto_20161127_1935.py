# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-27 19:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('podcasts', '0023_auto_20161026_0131'),
    ]

    operations = [
        migrations.AlterField(
            model_name='podcast',
            name='author_name',
            field=models.CharField(default='Anonymous', max_length=1024),
        ),
        migrations.AlterField(
            model_name='podcast',
            name='language',
            field=models.CharField(default='en-US', max_length=16),
        ),
        migrations.AlterField(
            model_name='podcast',
            name='subtitle',
            field=models.CharField(blank=True, default='', max_length=512),
        ),
        migrations.AlterField(
            model_name='podcastcategory',
            name='category',
            field=models.CharField(choices=[('Music/Easy Listening', 'Music/Easy Listening'), ('Music/Oldies', 'Music/Oldies'), ('Games & Hobbies', 'Games & Hobbies'), ('Government & Organizations/National', 'Government & Organizations/National'), ('TV & Film', 'TV & Film'), ('Music/Hip-Hop & Rap', 'Music/Hip-Hop & Rap'), ('Religion & Spirituality/Spirituality', 'Religion & Spirituality/Spirituality'), ('Music', 'Music'), ('Music/Electronic', 'Music/Electronic'), ('Arts/Performing Arts', 'Arts/Performing Arts'), ('Society & Culture/Personal Journals', 'Society & Culture/Personal Journals'), ('Government & Organizations/Local', 'Government & Organizations/Local'), ('Music/Electronic/Garage', 'Music/Electronic/Garage'), ('Music/Electronic/Breakbeat', 'Music/Electronic/Breakbeat'), ('Music/Electronic/Big Beat', 'Music/Electronic/Big Beat'), ('Comedy', 'Comedy'), ('Education/K-12', 'Education/K-12'), ('Sports & Recreation/College & High School', 'Sports & Recreation/College & High School'), ('Music/R&B & Urban', 'Music/R&B & Urban'), ('Music/Inspirational', 'Music/Inspirational'), ('Music/Soundtracks', 'Music/Soundtracks'), ('Music/Electronic/Downtempo', 'Music/Electronic/Downtempo'), ('Arts', 'Arts'), ('Music/Electronic/Jungle', 'Music/Electronic/Jungle'), ('Games & Hobbies/Other Games', 'Games & Hobbies/Other Games'), ('Technology/IT News', 'Technology/IT News'), ('Music/Electronic/Tribal', 'Music/Electronic/Tribal'), ('Business', 'Business'), ('Business/Investing', 'Business/Investing'), ('Education/Educational Technology', 'Education/Educational Technology'), ('Government & Organizations', 'Government & Organizations'), ('Music/Rock', 'Music/Rock'), ('Health/Self-Help', 'Health/Self-Help'), ('Technology/Podcasting', 'Technology/Podcasting'), ('Society & Culture/Places & Travel', 'Society & Culture/Places & Travel'), ('Games & Hobbies/Aviation', 'Games & Hobbies/Aviation'), ('Music/Electronic/Trip Hop', 'Music/Electronic/Trip Hop'), ('Games & Hobbies/Video Games', 'Games & Hobbies/Video Games'), ('Health/Kids & Family', 'Health/Kids & Family'), ('Technology', 'Technology'), ('Music/Blues', 'Music/Blues'), ('Music/Alternative', 'Music/Alternative'), ('Religion & Spirituality/Judaism', 'Religion & Spirituality/Judaism'), ('Religion & Spirituality', 'Religion & Spirituality'), ('Society & Culture', 'Society & Culture'), ('Music/Electronic/Disco', 'Music/Electronic/Disco'), ('Music/World', 'Music/World'), ('Education/Training', 'Education/Training'), ('Arts/Visual Arts', 'Arts/Visual Arts'), ('Music/Seasonal & Holiday', 'Music/Seasonal & Holiday'), ('Business/Shopping', 'Business/Shopping'), ('Health', 'Health'), ('Education', 'Education'), ('Music/Folk', 'Music/Folk'), ('Business/Management & Marketing', 'Business/Management & Marketing'), ('News & Politics/Conservative (Right)', 'News & Politics/Conservative (Right)'), ('News & Politics/Liberal (Left)', 'News & Politics/Liberal (Left)'), ('Arts/Design', 'Arts/Design'), ('Science & Medicine/Medicine', 'Science & Medicine/Medicine'), ('Arts/Literature', 'Arts/Literature'), ('Sports & Recreation/Amateur', 'Sports & Recreation/Amateur'), ('Society & Culture/Gay & Lesbian', 'Society & Culture/Gay & Lesbian'), ('Religion & Spirituality/Other', 'Religion & Spirituality/Other'), ('Religion & Spirituality/Hinduism', 'Religion & Spirituality/Hinduism'), ('Government & Organizations/Regional', 'Government & Organizations/Regional'), ('Arts/Food', 'Arts/Food'), ('Health/Sexuality', 'Health/Sexuality'), ('Health/Alternative Health', 'Health/Alternative Health'), ('Society & Culture/History', 'Society & Culture/History'), ('Technology/Software How-To', 'Technology/Software How-To'), ('Science & Medicine', 'Science & Medicine'), ('Music/Pop', 'Music/Pop'), ('Sports & Recreation', 'Sports & Recreation'), ('Government & Organizations/Non-Profit', 'Government & Organizations/Non-Profit'), ('Music/Electronic/Techno', 'Music/Electronic/Techno'), ('Music/New Age', 'Music/New Age'), ('Music/Electronic/House', 'Music/Electronic/House'), ('Games & Hobbies/Hobbies', 'Games & Hobbies/Hobbies'), ('Education/Higher Education', 'Education/Higher Education'), ('Music/Electronic/Trance', 'Music/Electronic/Trance'), ('Music/Country', 'Music/Country'), ('Science & Medicine/Social Sciences', 'Science & Medicine/Social Sciences'), ('Business/Careers', 'Business/Careers'), ('Music/Electronic/Ambient', 'Music/Electronic/Ambient'), ('Religion & Spirituality/Buddhism', 'Religion & Spirituality/Buddhism'), ('Games & Hobbies/Automotive', 'Games & Hobbies/Automotive'), ('Science & Medicine/Natural Sciences', 'Science & Medicine/Natural Sciences'), ('Religion & Spirituality/Islam', 'Religion & Spirituality/Islam'), ('Music/Electronic/IDM', 'Music/Electronic/IDM'), ('Music/Latin', 'Music/Latin'), ('Technology/Gadgets', 'Technology/Gadgets'), ('Society & Culture/Philosophy', 'Society & Culture/Philosophy'), ('Arts/Fashion & Beauty', 'Arts/Fashion & Beauty'), ('Sports & Recreation/Outdoor', 'Sports & Recreation/Outdoor'), ('Business/Business News', 'Business/Business News'), ('Health/Fitness & Nutrition', 'Health/Fitness & Nutrition'), ('Music/Electronic/Hard House', 'Music/Electronic/Hard House'), ('Music/Metal', 'Music/Metal'), ('Arts/Spoken Word', 'Arts/Spoken Word'), ('Music/Freeform', 'Music/Freeform'), ('Religion & Spirituality/Christianity', 'Religion & Spirituality/Christianity'), ('Music/Reggae', 'Music/Reggae'), ('Music/Electronic/Progressive', 'Music/Electronic/Progressive'), ('Music/Electronic/Acid House', 'Music/Electronic/Acid House'), ('News & Politics', 'News & Politics'), ('Education/Language Courses', 'Education/Language Courses'), ("Music/Electronic/Drum 'n' Bass", "Music/Electronic/Drum 'n' Bass"), ('Sports & Recreation/Professional', 'Sports & Recreation/Professional'), ('Music/Jazz', 'Music/Jazz')], max_length=128),
        ),
        migrations.AlterField(
            model_name='podcastepisode',
            name='description',
            field=models.TextField(default=''),
        ),
        migrations.AlterField(
            model_name='podcastepisode',
            name='duration',
            field=models.PositiveIntegerField(help_text='Audio duration in seconds'),
        ),
        migrations.AlterField(
            model_name='podcastepisode',
            name='explicit_override',
            field=models.CharField(choices=[('none', 'None'), ('expl', 'Explicit'), ('clen', 'Clean')], default='none', max_length=4),
        ),
        migrations.AlterField(
            model_name='podcastepisode',
            name='subtitle',
            field=models.CharField(blank=True, default='', max_length=1024),
        ),
    ]