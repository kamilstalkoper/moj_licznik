#!/usr/bin/env python
# encoding: utf-8

from __future__ import absolute_import

from app.subapps.structure.models import UserMeterPoint, Meter


def user_main_meter(request):
    context = {
        'cp_user_main_meter_point': None,
        'cp_user_meter_points': [],
    }
    if request.user.is_anonymous():
        return context

    user_meter_points = UserMeterPoint.objects.filter(user_id=request.user.id)

    for user_meter_point in user_meter_points:
        meter_point_dict = get_meter_data_dict(user_meter_point)
        if user_meter_point.is_main_meter_point:
            context['cp_user_main_meter_point'] = meter_point_dict

        context['cp_user_meter_points'].append(meter_point_dict)
    return context


def get_meter_data_dict(user_meter_point):
    related_meter = Meter.objects\
        .filter(
            meterpointstate__meter_point_id=user_meter_point.meter_point_id)\
        .last()

    if user_meter_point.alias:
        visible_name = user_meter_point.alias
    else:
        visible_name = related_meter.serial_number if related_meter else ''

    return {
        'visible_name': visible_name,
        'meter_point_id': user_meter_point.meter_point.id,
        'is_main_meter_point': user_meter_point.is_main_meter_point,
    }
