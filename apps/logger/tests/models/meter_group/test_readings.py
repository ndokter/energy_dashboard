from decimal import Decimal

import datetime
import pytz

from django.test import TestCase

from apps.logger.models.meter import Meter
from apps.logger.models.metric_total import MetricReportsQuerySet


class MeterGroupMetricsTestCase(TestCase):

    def setUp(self):
        self.tz = pytz.timezone('UTC')

        self.meter_tariff_1 = Meter.manager.electricity_used_tariff(1)
        self.meter_tariff_2 = Meter.manager.electricity_used_tariff(2)
        self.meter = self.meter_tariff_1.meter

        self.meter_tariff_1.prices.create(
            start=self.tz.localize(datetime.datetime(2015, 1, 1)),
            end=self.tz.localize(datetime.datetime(2016, 1, 1)),
            amount=0.25
        )
        self.meter_tariff_2.prices.create(
            start=self.tz.localize(datetime.datetime(2015, 1, 1)),
            end=self.tz.localize(datetime.datetime(2016, 1, 1)),
            amount=0.50
        )

        self.meter_tariff_1.metrics_total.create(
            datetime=self.tz.localize(datetime.datetime(2015, 1, 1)),
            value_total=Decimal('0')
        )
        self.meter_tariff_1.metrics_total.create(
            datetime=self.tz.localize(datetime.datetime(2015, 1, 2)),
            value_total=Decimal('1')
        )

        self.meter_tariff_2.metrics_total.create(
            datetime=self.tz.localize(datetime.datetime(2015, 1, 3)),
            value_total=Decimal('0')
        )
        self.meter_tariff_2.metrics_total.create(
            datetime=self.tz.localize(datetime.datetime(2015, 1, 4)),
            value_total=Decimal('2')
        )

    def test(self):
        result = self.meter.metrics_total()

        self.assertEqual(result.count(), 4)

    def test_datetime_aggregate(self):
        result = self.meter.metrics_total().datetime_aggregate(
            aggregate=MetricReportsQuerySet.YEAR
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
