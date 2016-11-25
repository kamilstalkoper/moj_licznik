#!/usr/bin/env python
# encoding: utf-8

from __future__ import absolute_import

from django.contrib import admin

from .models import Breakdown, Notice


class BreakdownAdmin(admin.ModelAdmin):
    list_display = ('id', 'start_at', 'end_at')
admin.site.register(Breakdown, BreakdownAdmin)


class NoticeAdmin(admin.ModelAdmin):
    list_display = ('title', )
admin.site.register(Notice, NoticeAdmin)
