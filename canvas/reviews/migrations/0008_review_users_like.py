# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-04-12 20:09
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('reviews', '0007_auto_20170410_2309'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='users_like',
            field=models.ManyToManyField(blank=True, related_name='reviews_liked', to=settings.AUTH_USER_MODEL),
        ),
    ]