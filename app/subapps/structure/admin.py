#!/usr/bin/env python
# encoding: utf-8

from __future__ import absolute_import

from django.contrib import admin

from .models import (
    Station, Meter, MeterPoint, TariffZone, TariffDefinition, MeterPointState,
    MeterObject, MeterData, Alarm)


class StationAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'serial_number', 'is_active')
    search_fields = ('name', 'serial_number')
admin.site.register(Station, StationAdmin)


class MeterAdmin(admin.ModelAdmin):
    list_display = ('serial_number', 'station', 'is_active', 'model_name')
    search_fields = ('model_name', 'serial_number')
admin.site.register(Meter, MeterAdmin)


class MeterPointAdmin(admin.ModelAdmin):
    list_display = ('name', 'ppe_code', 'station', 'is_active')
    search_fields = ('name', 'ppe_code')
admin.site.register(MeterPoint, MeterPointAdmin)


class TariffZoneAdmin(admin.ModelAdmin):
    list_display = ('name', 'obis')
    search_fields = ('name', 'obis')
admin.site.register(TariffZone, TariffZoneAdmin)


class TariffDefinitionAdmin(admin.ModelAdmin):
    list_display = ('tariff_zone', 'start_hour', 'end_hour')
    search_fields = ('tariff_zone', )
admin.site.register(TariffDefinition, TariffDefinitionAdmin)


class MeterPointStateAdmin(admin.ModelAdmin):
    list_display = ('meter', 'meter_point', 'start_at', 'end_at', 'start_value',
                    'current_power_limit', 'tariff_zone')
admin.site.register(MeterPointState, MeterPointStateAdmin)


class MeterObjectAdmin(admin.ModelAdmin):
    list_display = ('alias', 'obis', 'frequency', 'precision', 'unit')
admin.site.register(MeterObject, MeterObjectAdmin)


class MeterDataAdmin(admin.ModelAdmin):
    list_display = ('meter', 'value')
    search_fields = ('meter', )
admin.site.register(MeterData, MeterDataAdmin)


class AlarmAdmin(admin.ModelAdmin):
    list_display = ('meter', 'user', 'limit')
admin.site.register(Alarm, AlarmAdmin)
