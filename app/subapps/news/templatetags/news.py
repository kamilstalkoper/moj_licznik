#!/usr/bin/env python
# encoding: utf-8

from django import template


register = template.Library()


@register.filter
def strings_list_as_int_list(string_list):
    if not string_list:
        return []
    return [int(obj) for obj in string_list]
