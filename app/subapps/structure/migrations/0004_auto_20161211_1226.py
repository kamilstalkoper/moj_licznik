# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2016-12-11 11:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('structure', '0003_auto_20161211_1225'),
    ]

    operations = [
        migrations.AlterField(
            model_name='meterdata',
            name='flags',
            field=models.CharField(blank=True, max_length=32, null=True, verbose_name='Flagi'),
        ),
    ]
