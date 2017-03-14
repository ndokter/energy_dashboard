from django.db import models
from django.db.models import Avg

from apps.logger.models.datetime_aggregate_queryset import \
    DatetimeAggregateQuerySet
from apps.logger.models.meter import Meter


class ReadingActualQuerySet(DatetimeAggregateQuerySet):

    def datetime_aggregate(self, aggregate):

        return super(ReadingActualQuerySet, self)\
            .datetime_aggregate(aggregate) \
            .annotate(Avg('value'))


class ReadingActual(models.Model):
    objects = ReadingActualQuerySet.as_manager()

    meter = models.ForeignKey(Meter, related_name='readings_actual')

    datetime = models.DateTimeField()
    value = models.DecimalField(max_digits=8, decimal_places=3)

    class Meta(object):
        ordering = ['datetime']
        index_together = ['meter', 'datetime']
