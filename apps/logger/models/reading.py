from django.db import connections, models
from django.db.models.aggregates import Sum


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
            .extra(select={'datetime__aggregate': self.AGGREGATES[aggregate]})\
            .values('datetime__aggregate')\
            .annotate(Sum('value_increment'))

    @property
    def _engine(self):
        return connections.databases[self.db]['ENGINE']


class ElectricityReadingReportsQuerySet(ReadingReportsQuerySet):

    def datetime_aggregate(self, aggregate):

        return self\
            .extra(select={'datetime__aggregate': self.AGGREGATES[aggregate]})\
            .values('datetime__aggregate', 'tariff')\
            .annotate(Sum('value_increment'))


class AbstractReading(models.Model):
    objects = ReadingReportsQuerySet.as_manager()

    datetime = models.DateTimeField(db_index=True)
    value_increment = models.FloatField()
    value_total = models.FloatField()

    class Meta:
        abstract = True

    def save(self, **kwargs):
        # Calculate the increment from the previous record.
        last_record = self.__class__.objects \
            .filter(power_meter=self.power_meter) \
            .order_by('datetime') \
            .last()

        if last_record:
            self.value_increment = \
                self.value_total - last_record.value_total
        else:
            self.value_increment = 0

        return super(self.__class__, self).save(**kwargs)


class GasUsedReading(AbstractReading):
    pass


class ElectricityUsedReading(AbstractReading):
    objects = ElectricityReadingReportsQuerySet.as_manager()

    tariff = models.PositiveSmallIntegerField()


class ElectricityDeliveredReading(AbstractReading):
    objects = ElectricityReadingReportsQuerySet.as_manager()

    tariff = models.PositiveSmallIntegerField()
