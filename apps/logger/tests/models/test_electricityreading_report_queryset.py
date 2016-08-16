from decimal import Decimal

import datetime
import pytz

from django.test import TestCase

from apps.logger.models import ElectricityUsedReading as ElectricityReading
from apps.logger.models.abstract_reading import ReadingReportsQuerySet


class ElectricityReadingReportsQuerySetTestCase(TestCase):
    """
    Use ElectricityUsedReading which is a vanilla implementation of
    AbstractElectricityReading.
    """

    def setUp(self):
        self.tz = pytz.timezone('UTC')

        # Tariff 1 on 2015-12-31 (50 used)
        ElectricityReading.objects.create(
            tariff=1,
            value_total=Decimal('50'),
            datetime=self.tz.localize(datetime.datetime(2015, 12, 31, 23, 0))
        )
        ElectricityReading.objects.create(
            tariff=1,
            value_total=Decimal('100'),
            datetime=self.tz.localize(datetime.datetime(2015, 12, 31, 23, 59, 59))
        )

        # Tariff 1 on 2016-01-01 (550 used)
        ElectricityReading.objects.create(
            tariff=1,
            value_total=Decimal('600'),
            datetime=self.tz.localize(datetime.datetime(2016, 1, 1, 21, 0))
        )
        ElectricityReading.objects.create(
            tariff=1,
            value_total=Decimal('610'),
            datetime=self.tz.localize(datetime.datetime(2016, 1, 1, 21, 0, 10))
        )
        ElectricityReading.objects.create(
            tariff=1,
            value_total=Decimal('650'),
            datetime=self.tz.localize(datetime.datetime(2016, 1, 1, 21, 30))
        )
        # Tariff 2 on 2016-01-01 (10 used)
        ElectricityReading.objects.create(
            tariff=2,
            value_total=Decimal('800'),
            datetime=self.tz.localize(datetime.datetime(2016, 1, 1, 21, 59))
        )
        ElectricityReading.objects.create(
            tariff=2,
            value_total=Decimal('810'),
            datetime=self.tz.localize(datetime.datetime(2016, 1, 1, 22, 30))
        )

    def test_aggregate_second(self):
        result = ElectricityReading.objects\
            .datetime_aggregate(aggregate=ReadingReportsQuerySet.SECOND)

        self.assertListEqual(
            list(result),
            [
                {
                    'tariff': 1,
                    'datetime__aggregate': '2015-12-31T23:59:59',
                    'value_increment__sum': Decimal('50.0')
                },
                {
                    'tariff': 1,
                    'datetime__aggregate': '2016-01-01T21:00:00',
                    'value_increment__sum': Decimal('500.0')
                },
                {
                    'tariff': 1,
                    'datetime__aggregate': '2016-01-01T21:00:10',
                    'value_increment__sum': Decimal('10.0')
                },
                {
                    'tariff': 1,
                    'datetime__aggregate': '2016-01-01T21:30:00',
                    'value_increment__sum': Decimal('40.0')
                },
                {
                    'tariff': 2,
                    'datetime__aggregate': '2016-01-01T22:30:00',
                    'value_increment__sum': Decimal('10.0')
                }
            ]
        )

    def test_aggregate_hour(self):
        result = ElectricityReading.objects\
            .datetime_aggregate(aggregate=ReadingReportsQuerySet.HOUR)

        self.assertListEqual(
            list(result),
            [
                {
                    'tariff': 1,
                    'datetime__aggregate': '2015-12-31T23:00:00',
                    'value_increment__sum': Decimal('50.0')
                },
                {
                    'tariff': 1,
                    'datetime__aggregate': '2016-01-01T21:00:00',
                    'value_increment__sum': Decimal('550.0')
                },
                {
                    'tariff': 2,
                    'datetime__aggregate': '2016-01-01T22:00:00',
                    'value_increment__sum': Decimal('10.0')
                }
            ]
        )

    def test_aggregate_year(self):
        result = ElectricityReading.objects \
            .datetime_aggregate(aggregate=ReadingReportsQuerySet.YEAR)

        self.assertListEqual(
            list(result),
            [
                {
                    'tariff': 1,
                    'datetime__aggregate': '2015-01-01T00:00:00',
                    'value_increment__sum': Decimal('50.0')
                },
                {
                    'tariff': 1,
                    'datetime__aggregate': '2016-01-01T00:00:00',
                    'value_increment__sum': Decimal('550.0')
                },
                {
                    'tariff': 2,
                    'datetime__aggregate': '2016-01-01T00:00:00',
                    'value_increment__sum': Decimal('10.0')
                }
            ]
        )

