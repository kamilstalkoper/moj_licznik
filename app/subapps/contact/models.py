#!/usr/bin/env python
# encoding: utf-8

from __future__ import absolute_import

from django.contrib.auth.models import User
from django.db import models


class Problem(models.Model):
    user = models.ForeignKey(User, verbose_name=u'Użytkownik')

    electrician_needed = models.BooleanField(
        default=False, verbose_name=u'Żądanie elektryka?')
    solved = models.BooleanField(
        default=False, verbose_name=u'Problem rozwiązany?')

    class Meta:
        verbose_name = u'Problem'
        verbose_name_plural = u'Problemy'

    def __unicode__(self):
        return u'{} (Elektryk: {}) - ' \
               u'{}'.format(self.user.username, self.electrician_needed,
                            u'RZOWIĄZANY' if self.solved else u'W TRAKCIE')

    def get_last_message(self):
        return Message.objects.filter(problem=self.id).last()


class Message(models.Model):
    problem = models.ForeignKey(
        Problem, null=True, blank=True, verbose_name=u'Problem')
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name=u'Utworzona')

    content = models.TextField(verbose_name=u'Treść wiadomości')
    is_admin_replay = models.BooleanField(
        default=False, blank=True, verbose_name=u'Odpowiedź od administratora?')

    class Meta:
        verbose_name = u'Wiadomość'
        verbose_name_plural = u'Wiadomości'

    def __unicode__(self):
        return u'{}... ({})'.format(self.content[0:15], self.problem_id)
