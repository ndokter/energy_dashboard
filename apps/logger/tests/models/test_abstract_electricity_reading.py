from decimal import Decimal

import datetime
import pytz

from django.test import TestCase

from apps.logger.models import ElectricityUsedReading as ElectricityReading


class AbstractElectricityReadingTestCase(TestCase):
    """
    Use ElectricityUsedReading which is a vanilla implementation of
    AbstractElectricityReading.
    """

    def setUp(self):
        self.tz = pytz.timezone('UTC')

    def test_save(self):
        ElectricityReading.objects.create(
            tariff=1,
            value_total=Decimal('5'),
            datetime=self.tz.localize(datetime.datetime.now())
        )
        ElectricityReading.objects.create(
            tariff=2,
            value_total=Decimal('10'),
            datetime=self.tz.localize(datetime.datetime.now())
        )
        reading = ElectricityReading.objects.create(
            tariff=2,
            value_total=Decimal('10.123'),
            datetime=self.tz.localize(datetime.datetime.now())
        )

        self.assertEqual(reading.value_increment, Decimal('0.123'))

    def test_save_without_previous_record(self):
        reading = ElectricityReading.objects.create(
            tariff=1,
            value_total=Decimal('10'),
            datetime=self.tz.localize(datetime.datetime.now())
        )

        self.assertEqual(reading.value_increment, Decimal('0'))
