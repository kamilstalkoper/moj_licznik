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

    def get_period_class(self, number):
        for item in self.dct.values():
            if item[0] == number:
                return item[2]
        raise AttributeError


class AlarmPeriodType(object):
    def get_period(self, period_value):
        return NotImplementedError


class HoursAlarm(AlarmPeriodType):
    def get_period(self, period_value):
        start_at = now() + relativedelta(hours=-period_value)
        end_at = now()

        return start_at, end_at


class DaysAlarm(AlarmPeriodType):
    def get_period(self, period_value):
        start_at = now() + relativedelta(days=-period_value)
        end_at = now()

        return start_at, end_at


class WeeksAlarm(AlarmPeriodType):
    def get_period(self, period_value):
        start_at = now() + relativedelta(weeks=-period_value)
        end_at = now()

        return start_at, end_at


class MonthsAlarm(AlarmPeriodType):
    def get_period(self, period_value):
        start_at = now() + relativedelta(months=-period_value)
        end_at = now()

        return start_at, end_at

PERIOD_TYPES = PeriodEnum({
    'hours': (1, 'Godzin (-y)', HoursAlarm()),
    'days': (2, 'Doby / Dób', DaysAlarm()),
    'weeks': (3, 'Tygodnia (-dni)', WeeksAlarm()),
    'months': (4, 'Mieciąca (-cy)', MonthsAlarm()),
})
