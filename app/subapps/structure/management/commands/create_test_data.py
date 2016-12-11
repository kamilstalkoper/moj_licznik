#!/usr/bin/env python
# encoding: utf-8

from __future__ import absolute_import

from datetime import timedelta
import random

from django.core.management.base import BaseCommand
from django.utils import timezone

from app.subapps.structure.models import Meter, MeterObject, MeterData


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            '-d',
            dest='days',
            default=0,
            type=int,
            help=u'Dni liczba dni wstecz od dzisiaj, dla których mają być '
                 u'wygenerowane losowe dane.',
        )

        parser.add_argument(
            '-m',
            dest='meter_id',
            default=0,
            type=int,
            help=u'Id licznika, dla którego generowane będą dane. '
                 u'UWAGA!! Id != serial_number',
        )

    def handle(self, *args, **options):
        end_date = timezone.now()
        end_date = end_date.replace(hour=0, minute=0, second=0, microsecond=0)
        start_date = end_date - timedelta(days=options.get('days'))
        end_date += timedelta(days=1)

        self.stdout.write(u'Dodaję dane od {} do {}'.format(
            start_date.strftime('%d-%m-%Y %H:%M'),
            end_date.strftime('%d-%m-%Y %H:%M'))
        )

        meters = Meter.objects.all()
        if options.get('meter_id', 0) > 0:
            meters = meters.filter(id=options.get('meter_id'))

        meter_object, _ = MeterObject.objects.get_or_create(
            alias=u'Normalny',
            description=u'Pomiar normalny',
            obis=u'101',
            frequency=15,
            precision=10,
        )

        for meter in meters:
            self.stdout.write(
                u'Dodaję pomiary dla licznika {}'.format(meter.serial_number))
            meter_data_date = start_date
            last_meter_data = MeterData.objects.filter(
                meter_id=meter.id).last()
            last_meter_value = 0 if last_meter_data is None \
                else last_meter_data.value
            last_meter_date_acq_time = last_meter_data.acq_time \
                if last_meter_data is not None else None
            counter = 0

            while meter_data_date < end_date:
                if not last_meter_date_acq_time or meter_data_date > \
                        last_meter_date_acq_time:
                    counter += 1
                    last_meter_value += random.randint(0, 2)
                    MeterData.objects.create(
                        meter=meter,
                        meter_object=meter_object,
                        acq_time=meter_data_date,
                        scaler_scaler=2,
                        value=last_meter_value,
                    )
                meter_data_date += timedelta(minutes=15)
                self.stdout.write('.', ending='')

            self.stdout.write(
                u'\nKoniec generowania danych dla licznika\n'
                u'id: {}\n'
                u'serial_number: {}.\n'
                u'Dodano {} nowych danych.'
                u''.format(meter.id, meter.serial_number, counter))
