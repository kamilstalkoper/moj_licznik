#!/usr/bin/env python
# encoding: utf-8

from __future__ import absolute_import

from django import forms
from django.contrib.auth.models import User

from app.subapps.accounts.forms import RegistrationFirstStepForm
from app.subapps.structure.models import (
    Alarm, UserMeterPoint, MeterPoint, Meter)


class AddMeterForm(RegistrationFirstStepForm):
    set_as_main = forms.BooleanField(required=False)

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(AddMeterForm, self).__init__(*args, **kwargs)

    def clean(self):
        cd = super(AddMeterForm, self).clean()
        meter_serial_number = cd.get('meter_serial_number')
        ppe_code = cd.get('ppe_code')

        if not (meter_serial_number and ppe_code):
            # meter_serial_number or ppe_code invalid, do not need more
            # validation
            return cd

        if self.meter_point_state.meter_point.users.filter(id=self.user.id) \
                .exists():
            self.add_error('meter_serial_number', u'Masz już ten licznik.')

        return cd

    def save(self):
        UserMeterPoint.objects.create(
            user=self.user, meter_point=self.meter_point_state.meter_point)
        if self.cleaned_data.get('set_as_main', False) or not UserMeterPoint \
                .objects.filter(user_id=self.user.id, is_main_meter_point=True)\
                .exists():
            UserMeterPoint.objects \
                .filter(user_id=self.user.id, is_main_meter_point=True) \
                .update(is_main_meter_point=False)

            UserMeterPoint.objects\
                .filter(
                    user_id=self.user.id,
                    meter_point_id=self.meter_point_state.meter_point.id)\
                .update(is_main_meter_point=True)


class ChangeMainMeterForm(forms.Form):
    meter_point_id = forms.IntegerField()
    user_meter_point = None

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(ChangeMainMeterForm, self).__init__(*args, **kwargs)

    def clean(self):
        cd = super(ChangeMainMeterForm, self).clean()
        meter_point_id = cd.get('meter_point_id')

        if not meter_point_id:
            # meter_serial_number invalid
            return cd

        self.user_meter_point = UserMeterPoint.objects \
            .filter(meter_point_id=meter_point_id, user_id=self.user.id) \
            .first()

        if self.user_meter_point is None:
            self.add_error(
                'meter_point_id', u'Błędny numer punktu poboru energii.')
        elif self.user_meter_point.is_main_meter_point:
            self.add_error('meter_point_id',
                           u'Ten licznik jest już ustawiony jako główny.')

        return cd

    def save(self):
        UserMeterPoint.objects \
            .filter(user_id=self.user.id, is_main_meter_point=True) \
            .update(is_main_meter_point=False)

        UserMeterPoint.objects \
            .filter(
                user_id=self.user.id,
                meter_point_id=self.cleaned_data.get('meter_point_id')) \
            .update(is_main_meter_point=True)


class ChangeMeterUsersForm(forms.Form):
    users = forms.ModelMultipleChoiceField(
        queryset=User.objects.filter(is_active=True))

    def __init__(self, *args, **kwargs):
        self.meter_id = kwargs.pop('meter_id', None)
        super(ChangeMeterUsersForm, self).__init__(*args, **kwargs)

    def save(self):
        UserMeterPoint.objects \
            .filter(meter_point__meterpointstate__meter_id=self.meter_id) \
            .exclude(user__in=self.cleaned_data.get('users')) \
            .delete()

        meter_point = MeterPoint.objects.filter(
            meterpointstate__meter_id=self.meter_id).last()

        for user in self.cleaned_data.get('users'):
            UserMeterPoint.objects.get_or_create(
                meter_point=meter_point, user=user,
            )


class ChangeMeterAliasForm(forms.Form):
    meter_id = forms.IntegerField()
    alias = forms.CharField(max_length=255)

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(ChangeMeterAliasForm, self).__init__(*args, **kwargs)

    def clean_meter_id(self):
        meter_id = self.cleaned_data.get('meter_id')
        if not Meter.objects \
                .filter(meterpointstate__meter_point__users=self.user,
                        id=meter_id) \
                .exists():
            self.add_error('meter_id', u'Ten licznik nie należy do Ciebie.')

        return meter_id

    def save(self):
        UserMeterPoint.objects \
            .filter(
                meter_point__meterpointstate__meter_id=
                self.cleaned_data.get('meter_id'), user_id=self.user.id) \
            .update(alias=self.cleaned_data.get('alias'))


class AddAlarmForm(forms.ModelForm):
    class Meta:
        model = Alarm
        exclude = ['user', ]

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(AddAlarmForm, self).__init__(*args, **kwargs)
        self.fields['meter'].queryset = Meter.objects \
            .filter(meterpointstate__meter_point__users=self.user)

    def clean_meter(self):
        meter = self.cleaned_data.get('meter')
        if not Meter.objects \
                .filter(id=meter.id,
                        meterpointstate__meter_point__users=self.user) \
                .exists():
            self.add_error(
                'meter',
                u'Ten licznik nie należy do Ciebie.')

        return meter

    def save(self, commit=True):
        alarm = super(AddAlarmForm, self).save(commit=False)
        alarm.user = self.user
        alarm.save()

        return alarm
