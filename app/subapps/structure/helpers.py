#!/usr/bin/env python
# encoding: utf-8

from __future__ import absolute_import

from .enums.standard_enums import TARIFF_DEFINITION_TYPES
from .models import TariffDefinition


def get_tariff_data():
    tariff_definitions = TariffDefinition.objects.all().select_related('tariff')
    tariff_dict = {}
    for tariff_definition in tariff_definitions:
        if tariff_definition.tariff.name not in tariff_dict.keys():
            tariff_dict[tariff_definition.tariff.name] = {}

        tariff_type_description = TARIFF_DEFINITION_TYPES \
            .get_description_by_number(tariff_definition.tariff_type)
        if tariff_type_description not in \
                tariff_dict[tariff_definition.tariff.name]:
            tariff_dict[tariff_definition.tariff.name][
                tariff_type_description] = []

            tariff_dict[tariff_definition.tariff.name][
                tariff_type_description].append({
                    'start_hour': tariff_definition.start_hour,
                    'end_hour': tariff_definition.end_hour,
                })

    return tariff_dict
