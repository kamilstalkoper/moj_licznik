#!/usr/bin/env python
# encoding: utf-8

from __future__ import absolute_import

from django.contrib.auth.models import User
from django.db import models

from app.subapps.structure.models import Station


class Breakdown(models.Model):
    start_at = models.DateTimeField(verbose_name=u'Data rozpoczęcia')
    end_at = models.DateTimeField(verbose_name=u'Data zakończenia')
    reason = models.TextField(null=True, blank=True, verbose_name=u'Powód')

    stations = models.ManyToManyField(
        Station, verbose_name=u'Stacje objęte wyłączeniem')

    class Meta:
        verbose_name = u'Wyłączenie'
        verbose_name_plural = u'Wyłączenia'

    def __unicode__(self):
        return u'{} ({} -> {})'.format(self.id, self.start_at, self.end_at)


class Notice(models.Model):
    users = models.ManyToManyField(User, blank=True, verbose_name=u'Użytkownik')

    title = models.CharField(max_length=200, verbose_name=u'Tytuł')
    summary = models.CharField(max_length=500, verbose_name=u'Podsumowanie')

    content_body = models.TextField(verbose_name=u'Treść (markdown)')
    content_html = models.TextField(verbose_name=u'Treść HTML')

    breakdowns = models.ManyToManyField(
        Breakdown, blank=True, verbose_name=u'Powiązane przerwy w dostawie')

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = u'Ogłoszenie'
        verbose_name_plural = u'Ogłoszenia'

    def __unicode__(self):
        return u'{}{}'.format(self.title,
                              u' - Powiązane z wyłączeniem' if self.breakdowns
                              else u'')
