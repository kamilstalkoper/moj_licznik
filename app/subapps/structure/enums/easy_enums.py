#!/usr/bin/env python
# encoding: utf-8

from __future__ import absolute_import


class EasyEnum(object):
    def __init__(self, dct):
        self.dct = dct

    def __getattr__(self, item):
        if item in self.dct:
            return self.dct[item][0]
        raise AttributeError

    def as_enum(self):
        return self.dct.values()

    def get_number_by_description(self, description):
        for number, desc in self.dct.values():
            if desc == description:
                return number
        raise AttributeError

    def get_description_by_number(self, number):
        for num, description in self.dct.values():
            if num == number:
                return description
        raise AttributeError
