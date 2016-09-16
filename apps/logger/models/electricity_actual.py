from django.db import models

from apps.logger.models.datetime_aggregate_queryset import \
    DatetimeAggregateQuerySet
from apps.logger.models.meter import Meter


class ElectricityActual(models.Model):
    objects = DatetimeAggregateQuerySet.as_manager()

    meter = models.ForeignKey(Meter, related_name='electricity_actual')

    datetime = models.DateTimeField()
    value = models.DecimalField(max_digits=8, decimal_places=3)

    class Meta(object):
        ordering = ['datetime']
        index_together = ['meter', 'datetime']
