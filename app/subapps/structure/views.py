#!/usr/bin/env python
# encoding: utf-8

from __future__ import absolute_import

from django.views.generic import TemplateView


class HomeView(TemplateView):
    template_name = 'structure/home.html'
