#!/usr/bin/env python
# encoding: utf-8

from __future__ import absolute_import

from django import forms
from django.db.transaction import atomic

from .models import Message, Problem


class NewMessageForm(forms.Form):
    message_content = forms.CharField(widget=forms.Textarea())
    electrician_needed = forms.BooleanField(required=False)
    send_copy_to_me = forms.BooleanField(required=False)

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        self.problem = kwargs.pop('problem', None)
        self.is_admin_replay = kwargs.pop('is_admin_replay', False)
        super(NewMessageForm, self).__init__(*args, **kwargs)

    @atomic
    def save(self):
        cd = self.cleaned_data
        if self.problem is None:
            self.problem = Problem.objects.create(
                user=self.user,
                electrician_needed=cd.get('electrician_needed', False))

        message = Message.objects.create(
            problem=self.problem, content=cd.get('message_content', ''),
            is_admin_replay=self.is_admin_replay)

        return message
