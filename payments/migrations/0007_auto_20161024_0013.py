# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-10-24 00:13
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0006_auto_20161023_2339'),
    ]

    operations = [
        migrations.AddField(
            model_name='tipevent',
            name='recurring_tip',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='tip_events', to='payments.RecurringTip'),
        ),
        migrations.AlterField(
            model_name='recurringtip',
            name='stripe_customer_id',
            field=models.CharField(default='', max_length=128),
            preserve_default=False,
        ),
    ]