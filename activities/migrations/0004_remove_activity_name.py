# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-07 19:42
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('activities', '0003_auto_20171007_1638'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='activity',
            name='name',
        ),
    ]
