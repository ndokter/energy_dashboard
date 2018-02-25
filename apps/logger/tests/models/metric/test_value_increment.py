from decimal import Decimal

import datetime
import pytz

from django.test import TestCase

from apps.logger.models.meter import Meter
from apps.logger.models.metric_total import MetricReportsQuerySet


class MetricSaveValueIncrementTestCase(TestCase):

    def setUp(self):
        self.tz = pytz.timezone('UTC')

        self.meter = Meter.manager.electricity_used_tariff(0)

        self.meter.metrics_total.create(
            datetime=self.tz.localize(datetime.datetime(2015, 1, 1, 13, 0)),
            value_total=Decimal('0')
        )
        self.meter.metrics_total.create(
            datetime=self.tz.localize(datetime.datetime(2015, 1, 1, 14, 0)),
            value_total=Decimal('0.5')
        )
        self.meter.metrics_total.create(
            datetime=self.tz.localize(datetime.datetime(2015, 1, 1, 15, 0)),
            value_total=Decimal('1')
        )

        self.meter.metrics_total.create(
            datetime=self.tz.localize(datetime.datetime(2015, 1, 2, 13, 0)),
            value_total=Decimal('1.5')
        )
        self.meter.metrics_total.create(
            datetime=self.tz.localize(datetime.datetime(2015, 1, 2, 14, 0)),
            value_total=Decimal('2')
        )

    def test_single_day(self):
        result = self.meter.metrics_total\
            .filter(
                datetime__range=[
                    self.tz.localize(datetime.datetime(2015, 1, 1)),
                    self.tz.localize(datetime.datetime(2015, 1, 2))
                ]
            )\
            .datetime_aggregate(aggregate=ReadingReportsQuerySet.DAY)

        self.assertListEqual(
            list(result),
            [
                {
                    'datetime__aggregate': '2015-01-01T00:00:00',
                    'value_increment__sum': Decimal('1'),
                    'costs__sum': None
                }
            ]
        )

    def test_total(self):
        result = self.meter.metrics_total\
            .datetime_aggregate(aggregate=MetricReportsQuerySet.MONTH)

        self.assertListEqual(
            list(result),
            [
                {
                    'datetime__aggregate': '2015-01-01T00:00:00',
                    'value_increment__sum': Decimal('2'),
                    'costs__sum': None
                }
            ]
        )

