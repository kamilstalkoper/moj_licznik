# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-20 20:36
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('structure', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Breakdown',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_at', models.DateTimeField(verbose_name='Data rozpocz\u0119cia awarii')),
                ('end_at', models.DateTimeField(verbose_name='Data zako\u0144czenia awarii')),
                ('stations', models.ManyToManyField(to='structure.Station', verbose_name='Stacje obj\u0119te awari\u0105')),
            ],
            options={
                'verbose_name': 'Awaria',
                'verbose_name_plural': 'Awarie',
            },
        ),
        migrations.CreateModel(
            name='Notice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='Tytu\u0142')),
                ('summary', models.CharField(max_length=500, verbose_name='Podsumowanie')),
                ('content_body', models.TextField(verbose_name='Tre\u015b\u0107 (markdown)')),
                ('content_html', models.TextField(verbose_name='Tre\u015b\u0107 HTML')),
                ('breakdowns', models.ManyToManyField(blank=True, to='news.Breakdown', verbose_name='Powi\u0105zane przerwy w dostawie')),
                ('users', models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL, verbose_name='U\u017cytkownik')),
            ],
            options={
                'verbose_name': 'Og\u0142oszenie',
                'verbose_name_plural': 'Og\u0142oszenia',
            },
        ),
    ]