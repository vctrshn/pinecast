# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2015-12-17 07:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('podcasts', '0008_podcastepisode_description_flair'),
    ]

    operations = [
        migrations.AddField(
            model_name='podcastepisode',
            name='explicit_override',
            field=models.CharField(choices=[(b'none', 'None'), (b'expl', 'Explicit'), (b'clen', 'Clean')], default=b'none', max_length=4),
        ),
    ]