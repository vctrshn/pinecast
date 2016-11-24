# -*- coding: utf-8 -*-
from __future__ import absolute_import
# Generated by Django 1.9 on 2016-04-14 03:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0002_auto_20150726_1637'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assetimportrequest',
            name='audio_source_url',
            field=models.URLField(blank=True, max_length=500),
        ),
        migrations.AlterField(
            model_name='assetimportrequest',
            name='image_source_url',
            field=models.URLField(blank=True, max_length=500),
        ),
    ]
