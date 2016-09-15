from django.db import models
from django.db.models import Sum

from apps.logger.models.meter import MeterTariff


class ReadingReportsQuerySet(models.QuerySet):
    SECOND = 'second'
    MINUTE = 'minute'
    HOUR = 'hour'
    DAY = 'day'
    MONTH = 'month'
    YEAR = 'year'

    AGGREGATES = {
        SECOND: "strftime('%%Y-%%m-%%dT%%H:%%M:%%S', datetime)",
        MINUTE: "strftime('%%Y-%%m-%%dT%%H:%%M:00', datetime)",
        HOUR: "strftime('%%Y-%%m-%%dT%%H:00:00', datetime)",
        DAY: "strftime('%%Y-%%m-%%dT00:00:00', datetime)",
        MONTH: "strftime('%%Y-%%m-01T00:00:00', datetime)",
        YEAR: "strftime('%%Y-01-01T00:00:00', datetime)",
    }

    def datetime_aggregate(self, aggregate):
        return self\
            .extra(select={'datetime__aggregate': self.AGGREGATES[aggregate]}) \
            .values('datetime__aggregate') \
            .annotate(Sum('value_increment'), Sum('costs')) \
            .order_by('datetime__aggregate')


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
        price = self.meter.prices.active(self.datetime)

        if price:
            self.costs = self.value_increment * price.amount

        return super(Reading, self).save(**kwargs)
