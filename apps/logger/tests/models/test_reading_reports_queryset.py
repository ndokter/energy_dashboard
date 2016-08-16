from decimal import Decimal

import datetime
import pytz

from django.test import TestCase

from apps.logger.models import GasReading as Reading
from apps.logger.models.abstract_reading import ReadingReportsQuerySet


class ReadingReportsQuerySetTestCase(TestCase):
    """
    Used GasReading as it's currently the only unchanged implementation of
    AbstractReading.
    """

    def setUp(self):
        self.tz = pytz.timezone('UTC')

        # 2015-12-31 (50 used)
        Reading.objects.create(
            value_total=Decimal('50.000'),
            datetime=self.tz.localize(datetime.datetime(2015, 12, 31, 23, 0))
        )
        Reading.objects.create(
            value_total=Decimal('100.000'),
            datetime=self.tz.localize(datetime.datetime(2015, 12, 31, 23, 59, 59))
        )

        # 2016-01-01 (550 used)
        Reading.objects.create(
            value_total=Decimal('600.000'),
            datetime=self.tz.localize(datetime.datetime(2016, 1, 1, 21, 0))
        )
        Reading.objects.create(
            value_total=Decimal('650.000'),
            datetime=self.tz.localize(datetime.datetime(2016, 1, 1, 21, 30))
        )

    def test_aggregate_second(self):
        result = Reading.objects\
            .datetime_aggregate(aggregate=ReadingReportsQuerySet.SECOND)

        self.assertListEqual(
            list(result),
            [
                {
                    'datetime__aggregate': '2015-12-31T23:00:00',
                    'value_increment__sum': Decimal('0')
                },
                {
                    'datetime__aggregate': '2015-12-31T23:59:59',
                    'value_increment__sum': Decimal('50.000')
                },
                {
                    'datetime__aggregate': '2016-01-01T21:00:00',
                    'value_increment__sum': Decimal('500.000')
                },
                {
                    'datetime__aggregate': '2016-01-01T21:30:00',
                    'value_increment__sum': Decimal('50.000')
                }
            ]
        )

    def test_aggregate_hour(self):
        result = Reading.objects\
            .datetime_aggregate(aggregate=ReadingReportsQuerySet.HOUR)

        self.assertListEqual(
            list(result),
            [
                {
                    'datetime__aggregate': '2015-12-31T23:00:00',
                    'value_increment__sum': Decimal('50.000')
                },
                {
                    'datetime__aggregate': '2016-01-01T21:00:00',
                    'value_increment__sum': Decimal('550.000')
                },
            ]
        )

    def test_aggregate_year(self):
        result = Reading.objects \
            .datetime_aggregate(aggregate=ReadingReportsQuerySet.YEAR)

        self.assertListEqual(
            list(result),
            [
                {
                    'datetime__aggregate': '2015-01-01T00:00:00',
                    'value_increment__sum': Decimal('50.000')
                },
                {
                    'datetime__aggregate': '2016-01-01T00:00:00',
                    'value_increment__sum': Decimal('550.000')
                },
            ]
        )

