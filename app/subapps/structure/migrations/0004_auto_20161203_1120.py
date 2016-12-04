# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-12-03 10:20
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('structure', '0003_auto_20161125_1832'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='meter',
            name='users',
        ),
        migrations.AddField(
            model_name='meterpoint',
            name='users',
            field=models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL, verbose_name='U\u017cytkownicy'),
        ),
    ]