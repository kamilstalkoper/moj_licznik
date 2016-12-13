# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2016-12-11 11:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('structure', '0002_auto_20161211_1212'),
    ]

    operations = [
        migrations.AlterField(
            model_name='meterobject',
            name='unit',
            field=models.SmallIntegerField(choices=[(0, 'KWh'), (1, 'MWH')], default=0, verbose_name='Jednostka'),
        ),
    ]
