#!/usr/bin/env python
# encoding: utf-8

from __future__ import absolute_import

from dateutil.relativedelta import relativedelta

from django.utils.timezone import now

from .easy_enums import EasyEnum


class PeriodEnum(EasyEnum):
    def as_enum(self):
        return [
            (number, description) for number, description, _ in
            self.dct.values()
        ]

    def get_number_by_description(self, description):
        for number, desc, _ in self.dct.values():
            if desc == description:
                return number
        raise AttributeError

    def get_description_by_number(self, number):
        for num, description, _ in self.dct.values():
            if num == number:
                return description
        raise AttributeError

    def get_period_function(self, item):
        if item in self.dct:
            return self.dct[item][2]
        raise AttributeError


class AlarmPeriodType(object):
    def __init__(self):
        super(AlarmPeriodType, self).__init__()
        self.now = now()

    def get_period(self, period_value):
        return NotImplementedError


class HoursAlarm(AlarmPeriodType):
    def get_period(self, period_value):
        start_at = self.now - relativedelta(hours=-period_value)
        end_at = self.now

        return start_at, end_at


class DaysAlarm(AlarmPeriodType):
    def get_period(self, period_value):
        start_at = self.now.date() - relativedelta(days=-period_value)
        end_at = self.now.date()

        return start_at, end_at


class WeeksAlarm(AlarmPeriodType):
    def get_period(self, period_value):
        start_at = self.now.date() - relativedelta(weeks=-period_value)
        end_at = self.now.date()

        return start_at, end_at


class MonthsAlarm(AlarmPeriodType):
    def get_period(self, period_value):
        start_at = self.now.date() - relativedelta(months=-period_value)
        end_at = self.now.date()

        return start_at, end_at

PERIOD_TYPES = PeriodEnum({
    'hours': (1, 'Godzin (-y)', HoursAlarm),
    'days': (2, 'Doby / Dób', DaysAlarm),
    'weeks': (3, 'Tygodnia (-dni)', WeeksAlarm),
    'months': (4, 'Mieciąca (-cy)', MonthsAlarm),
})
