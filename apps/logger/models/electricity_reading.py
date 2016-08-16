from django.db import models
from django.db.models import Sum

from apps.logger.models.abstract_reading import ReadingReportsQuerySet, \
    AbstractReading


class ElectricityReadingReportsQuerySet(ReadingReportsQuerySet):

    def datetime_aggregate(self, aggregate):
        return self\
            .extra(select={'datetime__aggregate': self.AGGREGATES[aggregate]}) \
            .values('datetime__aggregate', 'tariff') \
            .annotate(Sum('value_increment')) \
            .exclude(value_increment=0) \
            .order_by('datetime__aggregate')


class AbstractElectricityReading(AbstractReading):
    objects = ElectricityReadingReportsQuerySet.as_manager()

    tariff = models.PositiveSmallIntegerField(db_index=True)

    class Meta(object):
        abstract = True
        index_together = ['tariff', 'datetime']

    def get_previous_record(self):
        return self.__class__.objects \
            .filter(datetime__lt=self.datetime, tariff=self.tariff) \
            .last()


class ElectricityUsedReading(AbstractElectricityReading):
    pass


class ElectricityDeliveredReading(AbstractElectricityReading):
    pass
