#!/usr/bin/env python
# encoding: utf-8

from __future__ import absolute_import

from django.contrib import admin

from .models import Problem, Message


class ProblemAdmin(admin.ModelAdmin):
    list_display = ('user', 'electrician_needed', 'solved')
    search_fields = ('user__username', 'user__email')
admin.site.register(Problem, ProblemAdmin)

admin.site.register(Message)
