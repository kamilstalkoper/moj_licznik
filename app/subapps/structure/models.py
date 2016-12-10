#!/usr/bin/env python
# encoding: utf-8

from __future__ import absolute_import

from django.contrib.auth.models import User
from django.db import models

from .enums.standard_enums import REASON_ENUMS, SCALER_UNIT_ENUMS
from .enums.period_enums import PERIOD_TYPES


class Station(models.Model):
    is_active = models.BooleanField(default=True, verbose_name=u'Aktywna?')

    address = models.CharField(max_length=255, null=True, blank=True,
                               verbose_name=u'Adres')
    name = models.CharField(max_length=255, null=True, blank=True,
                            verbose_name=u'Nazwa')
    serial_number = models.CharField(max_length=255, null=True, blank=True,
                                     verbose_name=u'Numer seryjny')

    class Meta:
        verbose_name = u'Stacja'
        verbose_name_plural = u'Stacje'

    def __unicode__(self):
        return u'{} ({})'.format(self.id, self.address)


class Meter(models.Model):
    model_name = models.CharField(null=True, blank=True, max_length=255,
                                  verbose_name=u'Nazwa modelu')
    serial_number = models.CharField(
        max_length=255, verbose_name=u'Numer seryjny')

    is_active = models.BooleanField(default=True, verbose_name=u'Aktywny?')
    detection_report_date = models.DateTimeField(
        verbose_name=u'Data wykrycia licznika przez AMI')
    station = models.ForeignKey(Station, verbose_name=u'Stacja')

    class Meta:
        verbose_name = u'Licznik'
        verbose_name_plural = u'Liczniki'

    def __unicode__(self):
        return u'{} [{}]'.format(self.serial_number, self.station)


class UserMeterPoint(models.Model):
    user = models.ForeignKey(User, verbose_name=u'Użytkownik')
    meter_point = models.ForeignKey('MeterPoint', verbose_name=u'Punkt pomiaru')

    is_main_meter_point = models.NullBooleanField(
        default=False, null=True, blank=True, verbose_name=u'Licznik główny?')
    alias = models.CharField(
        max_length=255, null=True, blank=True, verbose_name=u'Alias')

    class Meta:
        verbose_name = u'Punkt poboru energii - Użytkownik'
        verbose_name_plural = u'Punkty poboru energii - Użytkownicy'

    def __unicode__(self):
        return u'{} => {}'.format(self.user, self.meter_point)


class MeterPoint(models.Model):
    users = models.ManyToManyField(User, blank=True, through='UserMeterPoint',
                                   verbose_name=u'Użytkownicy')

    name = models.CharField(max_length=255, verbose_name=u'Nazwa')
    description = models.CharField(null=True, blank=True, max_length=500,
                                   verbose_name=u'Opis')
    address = models.CharField(null=True, blank=True, max_length=500,
                               verbose_name=u'Adres')
    ppe_code = models.CharField(max_length=255, verbose_name=u'Kod PPE')

    is_active = models.BooleanField(default=True, verbose_name=u'Aktywny?')
    flags = models.CharField(max_length=32, null=True, blank=True,
                             verbose_name=u'Flagi')

    station = models.ForeignKey(Station, verbose_name=u'Stacja')
    status_change_date = models.DateTimeField(
        verbose_name=u'Data ostatniej zmiany statusu')

    class Meta:
        verbose_name = u'Punkt pomiaru'
        verbose_name_plural = u'Punkty pomiaru'

    def __unicode__(self):
        return u'{} - {}'.format(self.name, self.ppe_code)


class TariffZone(models.Model):
    name = models.CharField(max_length=255, verbose_name=u'Nazwa strefy')
    obis = models.CharField(max_length=32)

    class Meta:
        verbose_name = u'Strefa czasowa'
        verbose_name_plural = u'Strefy czasowe'

    def __unicode__(self):
        return u'{} ({})'.format(self.name, self.obis)


class TariffDefinition(models.Model):
    start_hour = models.TimeField(verbose_name=u'Godzina startu')
    end_hour = models.TimeField(verbose_name=u'Godzina końca')

    tariff_zone = models.ForeignKey(TariffZone, verbose_name=u'Strefa czasowa')

    class Meta:
        verbose_name = u'Definicja strefy czasowej'
        verbose_name_plural = u'Definicje stref czasowych'

    def __unicode__(self):
        return u'{} - {} -> {}'.format(self.tariff_zone.name, self.start_hour,
                                       self.end_hour)


class MeterPointState(models.Model):
    meter = models.ForeignKey(Meter, verbose_name=u'Licznik')
    meter_point = models.ForeignKey(MeterPoint, verbose_name=u'Punkt pomiaru')

    start_at = models.DateTimeField(verbose_name=u'Rozpoczął działanie')
    end_at = models.DateTimeField(
        null=True, blank=True, verbose_name=u'Zakończył działanie')

    current_power_limit = models.IntegerField(verbose_name=u'Limit mocy')
    start_value = models.IntegerField(
        default=0, verbose_name=u'Wartość początkowa')

    tariff_zone = models.ForeignKey(TariffZone, verbose_name=u'Strefa czasowa')

    class Meta:
        verbose_name = u'Stan punktu pomiaru'
        verbose_name_plural = u'Stany punktów pomiarów'

    def __unicode__(self):
        return u'{} - {}'.format(self.meter, self.meter_point)


class MeterObject(models.Model):
    alias = models.CharField(max_length=255, verbose_name=u'Alias')
    description = models.CharField(max_length=500, verbose_name=u'Opis')

    obis = models.CharField(max_length=32, verbose_name=u'OBIS')
    frequency = models.SmallIntegerField(verbose_name=u'Częstotliwość')
    incremental_chart = models.BooleanField(
        default=True,
        verbose_name=u'Czy wartość w stosunku do poprzednego pomiaru wzrosła?')
    precision = models.SmallIntegerField(verbose_name=u'Precyzja')

    unit = models.SmallIntegerField(verbose_name=u'Jednostka')

    class Meta:
        verbose_name = u'Obiekt pomiaru'
        verbose_name_plural = u'Obiekty pomiarów'

    def __unicode__(self):
        return u'{} ({})'.format(self.alias, self.obis)


class MeterData(models.Model):
    meter = models.ForeignKey(Meter, verbose_name=u'Licznik')
    meter_object = models.ForeignKey(
        MeterObject, verbose_name=u'Obiekt pomiaru')

    acq_time = models.DateTimeField(verbose_name=u'Data pomiaru')
    cap_time = models.IntegerField(
        default=15, verbose_name=u'Częstotliwość pomiaru (minuty)')

    flags = models.CharField(max_length=32, verbose_name=u'Flagi')
    reason = models.SmallIntegerField(
        default=REASON_ENUMS.auto, choices=REASON_ENUMS.as_enum(),
        verbose_name=u'Typ pomiaru')
    scaler_scaler = models.IntegerField(verbose_name=u'Wartość normalizacji')
    scaler_unit = models.SmallIntegerField(
        choices=SCALER_UNIT_ENUMS.as_enum(), default=SCALER_UNIT_ENUMS.KWh,
        verbose_name=u'Jednostka')

    value = models.BigIntegerField(verbose_name=u'Wartość pomiaru')

    class Meta:
        verbose_name = u'Pomiar'
        verbose_name_plural = u'Pomiary'

    def __unicode__(self):
        return u'{}: {}'.format(self.meter, self.value)


class Alarm(models.Model):
    meter = models.ForeignKey(Meter, verbose_name=u'Licznik')
    user = models.ForeignKey(User, verbose_name=u'Użytkownik')

    limit = models.IntegerField(verbose_name=u'Limit')

    period = models.IntegerField(verbose_name=u'Okres')
    period_type = models.SmallIntegerField(
        choices=PERIOD_TYPES.as_enum(), verbose_name=u'Typ okresu')

    class Meta:
        verbose_name = u'Alarm'
        verbose_name_plural = u'Alarmy'

    def __unicode__(self):
        return u'{} ({})'.format(self.user.username, self.limit)
