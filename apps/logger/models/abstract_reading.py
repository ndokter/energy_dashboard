from django.db import models
from django.db.models import Sum


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
            .annotate(Sum('value_increment')) \
            .order_by('datetime__aggregate')


class AbstractReading(models.Model):
    objects = ReadingReportsQuerySet.as_manager()

    datetime = models.DateTimeField(db_index=True)
    value_increment = models.DecimalField(max_digits=8, decimal_places=3)
    value_total = models.DecimalField(max_digits=9, decimal_places=3)
    costs = models.DecimalField(max_digits=9, decimal_places=3, null=True)

    class Meta:
        abstract = True
        ordering = ['datetime']

    def get_previous_record(self):
        return self.__class__.objects \
            .filter(datetime__lt=self.datetime) \
            .last()

    def save(self, **kwargs):
        last_record = self.get_previous_record()

        if last_record:
            self.value_increment = \
                self.value_total - last_record.value_total
        else:
            self.value_increment = 0

        return super(AbstractReading, self).save(**kwargs)
