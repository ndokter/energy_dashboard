from django.core.management import BaseCommand

from apps.logger.models import Meter
from dsmr_reader.obis_references import P1_MESSAGE_TIMESTAMP, \
    ELECTRICITY_ACTIVE_TARIFF, ELECTRICITY_USED_TARIFF_ALL, \
    ELECTRICITY_DELIVERED_TARIFF_ALL, HOURLY_GAS_METER_READING
from dsmr_reader.readers.v4 import SerialReader as DSMR4SerialReader


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('device', type=str)

    def handle(self, *args, **options):
        serial_reader = DSMR4SerialReader(options['device'])

        for telegram in serial_reader.read():
            message_datetime = telegram[P1_MESSAGE_TIMESTAMP]

            tariff = telegram[ELECTRICITY_ACTIVE_TARIFF]

            electricity_used_total \
                = telegram[ELECTRICITY_USED_TARIFF_ALL[tariff - 1]]
            electricity_delivered_total = \
                telegram[ELECTRICITY_DELIVERED_TARIFF_ALL[tariff - 1]]

            gas_reading = telegram[HOURLY_GAS_METER_READING]

            Meter.register_electricity_used(
                value_total=electricity_used_total.value,
                datetime=message_datetime.value,
                tariff=tariff.value
            )

            if electricity_delivered_total.value:
                Meter.register_electricity_delivered(
                    value_total=electricity_delivered_total.value,
                    datetime=message_datetime.value,
                    tariff=tariff.value
                )

            is_new_gas_reading = not Meter.get_gas_meter().readings\
                .filter(datetime__gte=gas_reading.datetime) \
                .exists()

            if is_new_gas_reading:
                Meter.register_gas_used(
                    value_total=gas_reading.value,
                    datetime=gas_reading.datetime
                )

