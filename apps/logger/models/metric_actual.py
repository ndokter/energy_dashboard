from django.db import models
from django.db.models import Avg

from apps.logger.models.datetime_aggregate_queryset import \
    DatetimeAggregateQuerySet
from apps.logger.models.meter import Meter


class MetricActualQuerySet(DatetimeAggregateQuerySet):

    def datetime_aggregate(self, aggregate):
        return super(MetricActualQuerySet, self)\
            .datetime_aggregate(aggregate) \
            .annotate(Avg('value'))


class MetricActual(models.Model):
    objects = MetricActualQuerySet.as_manager()

    meter = models.ForeignKey(Meter, related_name='metrics_actual', on_delete=models.PROTECT)

    datetime = models.DateTimeField()
    value = models.DecimalField(max_digits=8, decimal_places=3)

    class Meta(object):
        ordering = ['datetime']
        index_together = ['meter', 'datetime']
