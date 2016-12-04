#!/usr/bin/env python
# encoding: utf-8

from app.subapps.structure.models import UserMainMeterPoint, Meter


def user_main_meter(request):
    none_dict = {
        'user_main_meter': None,
        'user_meters': None,
    }
    if request.user.is_anonymous():
        return none_dict

    main_meter_point = UserMainMeterPoint.objects \
        .filter(user_id=request.user.id) \
        .first()
    if main_meter_point is None or main_meter_point.meter_point is None:
        return none_dict

    main_meter = Meter.objects \
        .filter(meterpointstate__meter_point_id=main_meter_point.meter_point.id,
                meterpointstate__meter_point__users=request.user) \
        .first()
    user_meters = Meter.objects \
        .filter(meterpointstate__meter_point__users=request.user)

    return {
        'cp_user_main_meter': None if main_meter is None else main_meter,
        'cp_user_meters': user_meters,
    }
