from django.db import models
from django.db.models import Sum

from apps.logger.models.datetime_aggregate_queryset import \
    DatetimeAggregateQuerySet
from apps.logger.models.meter_tariff import MeterTariff


class ReadingReportsQuerySet(DatetimeAggregateQuerySet):

    def datetime_aggregate(self, aggregate):
        return super(ReadingReportsQuerySet, self)\
            .datetime_aggregate(aggregate) \
            .annotate(Sum('value_increment'), Sum('costs'))


class Reading(models.Model):
    objects = ReadingReportsQuerySet.as_manager()

    meter_tariff = models.ForeignKey(MeterTariff, related_name='readings')

    datetime = models.DateTimeField()
    value_increment = models.DecimalField(max_digits=8, decimal_places=3)
    value_total = models.DecimalField(max_digits=9, decimal_places=3)
    costs = models.DecimalField(max_digits=9, decimal_places=4, null=True)

    class Meta(object):
        ordering = ['datetime']
        index_together = ['meter_tariff', 'datetime']

    def save(self, **kwargs):
        last_record = Reading.objects \
            .filter(
                datetime__lt=self.datetime,
                meter_tariff=self.meter_tariff
            ) \
            .last()

        # Calculate increment.
        if last_record:
            self.value_increment = self.value_total - last_record.value_total
        else:
            self.value_increment = 0

        # Calculate costs based on the price that is active when the record
        # counts (based on it's datetime).
        price = self.meter_tariff.prices.active(self.datetime)

        if price:
            self.costs = self.value_increment * price.amount

        return super(Reading, self).save(**kwargs)
