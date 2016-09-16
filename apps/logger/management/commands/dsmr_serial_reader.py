from django.core.management import BaseCommand

from dsmr_parser.obis_references import P1_MESSAGE_TIMESTAMP, \
    ELECTRICITY_ACTIVE_TARIFF, ELECTRICITY_USED_TARIFF_ALL, \
    ELECTRICITY_DELIVERED_TARIFF_ALL, HOURLY_GAS_METER_READING, \
    CURRENT_ELECTRICITY_USAGE, CURRENT_ELECTRICITY_DELIVERY
from dsmr_parser import telegram_specifications
from dsmr_parser.serial import SerialReader, SERIAL_SETTINGS_V4

from apps.logger.models.meter import MeterManager


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('device', type=str)

    def handle(self, *args, **options):
        serial_reader = SerialReader(
            device=options['device'],
            serial_settings=SERIAL_SETTINGS_V4,
            telegram_specification=telegram_specifications.V4
        )

        for telegram in serial_reader.read():
            message_datetime = telegram[P1_MESSAGE_TIMESTAMP]

            tariff = telegram[ELECTRICITY_ACTIVE_TARIFF]
            tariff = int(tariff.value)

            electricity_used_total \
                = telegram[ELECTRICITY_USED_TARIFF_ALL[tariff - 1]]
            electricity_delivered_total = \
                telegram[ELECTRICITY_DELIVERED_TARIFF_ALL[tariff - 1]]

            electricity_used_actual = \
                telegram[CURRENT_ELECTRICITY_USAGE]
            electricity_delivered_actual = \
                telegram[CURRENT_ELECTRICITY_DELIVERY]

            gas_reading = telegram[HOURLY_GAS_METER_READING]

            is_new_gas_reading = not MeterManager().gas_tariff().readings\
                .filter(datetime__gte=gas_reading.datetime)\
                .exists()

            MeterManager().electricity_used().electricity_actual.create(
                datetime=message_datetime.value,
                value=electricity_used_actual
            )
            MeterManager().electricity_used_tariff(tariff).readings.create(
                datetime=message_datetime.value,
                value_total=electricity_used_total.value
            )

            if electricity_delivered_total.value:
                MeterManager().electricity_used().electricity_delivered.create(
                    datetime=message_datetime.value,
                    value=electricity_delivered_actual
                )
                MeterManager().electricity_delivered_tariff(tariff).readings.create(
                    datetime=message_datetime.value,
                    value_total=electricity_delivered_total.value
                )

            if is_new_gas_reading:
                MeterManager().gas_tariff().readings.create(
                    value_total=gas_reading.value,
                    datetime=gas_reading.datetime
                )
