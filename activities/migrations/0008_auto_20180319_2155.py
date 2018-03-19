# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-03-19 18:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activities', '0007_auto_20180313_1042'),
    ]

    operations = [
        migrations.AddField(
            model_name='users',
            name='bitbucket',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='users',
            name='passwordbit',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='users',
            name='svn',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='users',
            name='accesstoken',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='users',
            name='githubid',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
    ]
