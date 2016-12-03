#!/usr/bin/env python
# encoding: utf-8

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.db.transaction import atomic

from app.subapps.structure.models import MeterPointState


class RegistrationFirstStepForm(forms.Form):
    meter_serial_number = forms.CharField(max_length=255)
    ppe_code = forms.CharField(max_length=255)
    meter_point_state = None

    def clean(self):
        cd = super(RegistrationFirstStepForm, self).clean()

        meter_serial_number = cd.get('meter_serial_number')
        ppe_code = cd.get('ppe_code')

        if not (meter_serial_number and ppe_code):
            # meter_serial_number or ppe_code invalid, do not need more
            # validation
            return cd

        # check if meter_serial_number and ppe_code are valid
        self.meter_point_state = MeterPointState.objects \
            .filter(meter_point__ppe_code=ppe_code,
                    meter__serial_number=meter_serial_number) \
            .first()

        if self.meter_point_state is None:
            self.add_error(
                'ppe_code',
                u'Numer seryjny licznika lub kod PPE nie są prawidłowe.'
            )

        return cd


class RegistrationSecondStepForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email')

    def __init__(self, *args, **kwargs):
        self.meter_point_state = kwargs.pop('meter_point_state', None)
        super(RegistrationSecondStepForm, self).__init__(*args, **kwargs)

    @atomic
    def save(self, commit=True):
        user = super(RegistrationSecondStepForm, self).save()
        user.email = self.cleaned_data.get('email')
        user.save()

        self.meter_point_state.meter_point.users.add(user)

        return user
