# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-10-26 01:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0010_auto_20160414_0301'),
    ]

    operations = [
        migrations.AlterField(
            model_name='network',
            name='created',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]