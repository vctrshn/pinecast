# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-12-27 07:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0014_auto_20161214_0546'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usersettings',
            name='coupon_code',
            field=models.CharField(blank=True, max_length=16, null=True),
        ),
    ]
