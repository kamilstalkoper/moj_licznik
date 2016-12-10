# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2016-12-10 10:32
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Utworzona')),
                ('content', models.TextField(verbose_name='Tre\u015b\u0107 wiadomo\u015bci')),
                ('is_admin_replay', models.BooleanField(default=False, verbose_name='Odpowied\u017a od administratora?')),
            ],
            options={
                'verbose_name': 'Wiadomo\u015b\u0107',
                'verbose_name_plural': 'Wiadomo\u015bci',
            },
        ),
        migrations.CreateModel(
            name='Problem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('electrician_needed', models.BooleanField(default=False, verbose_name='\u017b\u0105danie elektryka?')),
                ('solved', models.BooleanField(default=False, verbose_name='Problem rozwi\u0105zany?')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='U\u017cytkownik')),
            ],
            options={
                'verbose_name': 'Problem',
                'verbose_name_plural': 'Problemy',
            },
        ),
        migrations.AddField(
            model_name='message',
            name='problem',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='contact.Problem', verbose_name='Problem'),
        ),
    ]
