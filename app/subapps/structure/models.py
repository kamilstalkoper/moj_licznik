#!/usr/bin/env python
# encoding: utf-8

from django.contrib.auth.models import User
from django.db import models


class Station(models.Model):
    is_active = models.BooleanField(default=True, verbose_name=u'Aktywna?')

    address = models.CharField(max_length=255, null=True, blank=True, verbose_name=u'Adres')
    name = models.CharField(max_length=255, null=True, blank=True, verbose_name=u'Nazwa')
    serial_number = models.CharField(max_length=255, null=True, blank=True, verbose_name=u'Numer seryjny')

    class Meta:
        verbose_name = u'Stacja'
        verbose_name_plural = u'Stacje'

    def __unicode__(self):
        return u'{} ({})'.format(self.id, self.address)
