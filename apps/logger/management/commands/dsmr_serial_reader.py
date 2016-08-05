from django.core.management import BaseCommand

from apps.logger.models import PowerMeter
from dsmr_reader.obis_references import P1_MESSAGE_TIMESTAMP, \
    ELECTRICITY_ACTIVE_TARIFF, ELECTRICITY_USED_TARIFF_ALL, \
    ELECTRICITY_DELIVERED_TARIFF_ALL, HOURLY_GAS_METER_READING
from dsmr_reader.readers.v4 import SerialReader as DSMR4SerialReader


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('device', type=str)

    def handle(self, *args, **options):

        meter_gas = PowerMeter.objects.get_or_create(
            name='gas',
            unit=PowerMeter.UNIT_M3
        )[0]

        serial_reader = DSMR4SerialReader(options['device'])

        for telegram in serial_reader.read():

            message_datetime = telegram[P1_MESSAGE_TIMESTAMP]

            tariff = telegram[ELECTRICITY_ACTIVE_TARIFF]
            tariff = int(tariff.value)

            electricity_used_meter = PowerMeter.objects.get_or_create(
                name='t{}_used'.format(tariff),
                unit=PowerMeter.UNIT_KWH
            )[0]

            electricity_used_total \
                = telegram[ELECTRICITY_USED_TARIFF_ALL[tariff - 1]]
            # electricity_used_actual \
            #     = telegram[CURRENT_ELECTRICITY_USAGE]

            electricity_delivered_total = \
                telegram[ELECTRICITY_DELIVERED_TARIFF_ALL[tariff - 1]]
            # electricity_delivered_actual = \
            #     telegram[CURRENT_ELECTRICITY_DELIVERY]

            gas_reading = telegram[HOURLY_GAS_METER_READING]

            electricity_used_meter.readings.create(
                value_total=electricity_used_total.value,
                datetime=message_datetime.value
            )

            if electricity_delivered_total.value:
                electricity_delivered_meter = PowerMeter.objects.get_or_create(
                    name='t{}_delivered'.format(tariff),
                    unit=PowerMeter.UNIT_KWH
                )[0]

                electricity_delivered_meter.readings.create(
                    value_total=electricity_delivered_total.value,
                    datetime=message_datetime.value)

            is_new_gas_reading = not meter_gas.readings\
                .filter(datetime__gte=gas_reading.datetime) \
                .exists()

            if is_new_gas_reading:
                meter_gas.readings.create(
                    value_total=gas_reading.value,
                    datetime=gas_reading.datetime
                )

