#!/usr/bin/env python
# encoding: utf-8

from __future__ import absolute_import

from .easy_enums import EasyEnum

REASON_ENUMS = EasyEnum({
    'auto': (0, u'Pomiar Automatyczny'),
    'manual': (1, u'Wartość wprowadzona ręcznie'),
})

SCALER_UNIT_ENUMS = EasyEnum({
    'KWh': (0, u'KWh'),
    'MWh': (1, u'MWH'),
})
