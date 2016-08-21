from decimal import Decimal

import datetime
import pytz

from django.test import TestCase

from apps.logger.models.meter import Meter, MeterGroup
from apps.logger.models.reading import ReadingReportsQuerySet


class MeterGroupReadingsTestCase(TestCase):

    def setUp(self):
        self.tz = pytz.timezone('UTC')

        self.meter_group = MeterGroup.objects.create(slug='test')

        self.meter_1 = Meter.objects.create(
            meter_group=self.meter_group,
            slug='meter-1',
            unit=Meter.UNIT_KWH
        )
        self.meter_2 = Meter.objects.create(
            meter_group=self.meter_group,
            slug='meter-2',
            unit=Meter.UNIT_M3
        )

        self.meter_1.prices.create(
            start=self.tz.localize(datetime.datetime(2015, 1, 1)),
            end=self.tz.localize(datetime.datetime(2016, 1, 1)),
            amount=0.25
        )
        self.meter_2.prices.create(
            start=self.tz.localize(datetime.datetime(2015, 1, 1)),
            end=self.tz.localize(datetime.datetime(2016, 1, 1)),
            amount=0.50
        )

        self.meter_1.readings.create(
            datetime=self.tz.localize(datetime.datetime(2015, 1, 1)),
            value_total=Decimal('0')
        )
        self.meter_1.readings.create(
            datetime=self.tz.localize(datetime.datetime(2015, 1, 2)),
            value_total=Decimal('1')
        )

        self.meter_2.readings.create(
            datetime=self.tz.localize(datetime.datetime(2015, 1, 3)),
            value_total=Decimal('0')
        )
        self.meter_2.readings.create(
            datetime=self.tz.localize(datetime.datetime(2015, 1, 4)),
            value_total=Decimal('2')
        )

    def test(self):
        result = self.meter_group.readings()

        self.assertEqual(result.count(), 4)

    def test_datetime_aggregate(self):
        result = self.meter_group.readings().datetime_aggregate(
            aggregate=ReadingReportsQuerySet.YEAR
        )

        self.assertListEqual(
            list(result),
            [
                {
                    'datetime__aggregate': '2015-01-01T00:00:00',
                    'value_increment__sum': Decimal('3.000'),
                    'costs__sum': Decimal('1.250')
                }
            ]
        )
