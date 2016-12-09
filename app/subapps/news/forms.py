#!/usr/bin/env python
# encoding: utf-8

from __future__ import absolute_import
from markdown import markdown

from django import forms

from .models import Notice, Breakdown


class CreateNoticeForm(forms.ModelForm):
    class Meta:
        model = Notice
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(CreateNoticeForm, self).__init__(*args, **kwargs)
        self.fields['content_html'].required = False

    def save(self, commit=True):
        notice = super(CreateNoticeForm, self).save(commit=False)
        notice.content_html = markdown(notice.content_body)
        notice.save()

        for user in self.cleaned_data.get('users', []):
            notice.users.add(user)

        for breakdown in self.cleaned_data.get('breakdowns', []):
            notice.breakdowns.add(breakdown)

        return notice


class CreateBreakdownForm(forms.ModelForm):
    class Meta:
        model = Breakdown
        fields = '__all__'
