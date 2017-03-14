from django.core.management import BaseCommand

from dsmr_parser.obis_references import P1_MESSAGE_TIMESTAMP, \
    ELECTRICITY_ACTIVE_TARIFF, ELECTRICITY_USED_TARIFF_ALL, \
    ELECTRICITY_DELIVERED_TARIFF_ALL, HOURLY_GAS_METER_READING, \
    CURRENT_ELECTRICITY_USAGE, CURRENT_ELECTRICITY_DELIVERY
from dsmr_parser import telegram_specifications
from dsmr_parser.clients import SerialReader, SERIAL_SETTINGS_V4

from apps.logger.models.meter import Meter


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

            electricity_used_tariff = \
                Meter.manager.electricity_used_tariff(tariff)
            electricity_delivered_tariff = \
                Meter.manager.electricity_delivered_tariff(tariff)
            gas_tariff = Meter.manager.gas_tariff()

            Meter.manager.electricity_used().readings_actual.create(
                datetime=message_datetime.value,
                value=electricity_used_actual.value
            )

            if _is_new_hourly_reading(electricity_used_tariff,
                                      message_datetime.value):
                electricity_used_tariff.readings_total.create(
                    datetime=message_datetime.value,
                    value_total=electricity_used_total.value
                )

            if electricity_delivered_total.value:
                Meter.manager.electricity_delivered().readings_actual.create(
                    datetime=message_datetime.value,
                    value=electricity_delivered_actual.value
                )

                if _is_new_hourly_reading(electricity_delivered_tariff,
                                          message_datetime.value):
                    electricity_delivered_tariff.readings_total.create(
                        datetime=message_datetime.value,
                        value_total=electricity_delivered_total.value
                    )

            if _is_new_hourly_reading(gas_tariff, gas_reading.datetime):
                gas_tariff.readings_total.create(
                    value_total=gas_reading.value,
                    datetime=gas_reading.datetime
                )


def _is_new_hourly_reading(meter_tariff, reading_datetime):
    reading_datetime = reading_datetime\
        .replace(minute=0, second=0, microsecond=0)

    return not meter_tariff.readings_total\
        .filter(datetime__gte=reading_datetime)\
        .exists()
