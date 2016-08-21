from decimal import Decimal
from django.core.management import BaseCommand

from dsmr_reader.obis_references import P1_MESSAGE_TIMESTAMP, \
    ELECTRICITY_ACTIVE_TARIFF, ELECTRICITY_USED_TARIFF_ALL, \
    ELECTRICITY_DELIVERED_TARIFF_ALL, HOURLY_GAS_METER_READING
from dsmr_reader.readers.v4 import SerialReader as DSMR4SerialReader

from apps.logger.models.meter import MeterGroup


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('device', type=str)

    def handle(self, *args, **options):
        serial_reader = DSMR4SerialReader(options['device'])

        for telegram in serial_reader.read():
            message_datetime = telegram[P1_MESSAGE_TIMESTAMP]

            tariff = telegram[ELECTRICITY_ACTIVE_TARIFF]
            tariff = int(tariff.value)

            electricity_used_total \
                = telegram[ELECTRICITY_USED_TARIFF_ALL[tariff - 1]]
            electricity_delivered_total = \
                telegram[ELECTRICITY_DELIVERED_TARIFF_ALL[tariff - 1]]

            gas_reading = telegram[HOURLY_GAS_METER_READING]

            is_new_gas_reading = not MeterGroup.meter.gas().readings\
                .filter(datetime__gte=gas_reading.datetime)\
                .exists()

            MeterGroup.meter.electricity_used(tariff).readings.create(
                datetime=message_datetime.value,
                value_total=Decimal(electricity_used_total.value)
            )

            if electricity_delivered_total.value:
                MeterGroup.meter.electricity_delivered(tariff).readings.create(
                    datetime=message_datetime.value,
                    value_total=Decimal(electricity_delivered_total.value)
                )

            if is_new_gas_reading:
                MeterGroup.meter.gas().readings.create(
                    value_total=Decimal(gas_reading.value),
                    datetime=gas_reading.datetime
                )
