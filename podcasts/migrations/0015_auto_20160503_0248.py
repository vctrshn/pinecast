# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-05-03 02:48
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('podcasts', '0014_auto_20160503_0247'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='podcast',
            name='tip_last_payout',
        ),
        migrations.RemoveField(
            model_name='podcast',
            name='tip_last_payout_amount',
        ),
        migrations.RemoveField(
            model_name='podcast',
            name='tip_value',
        ),
    ]