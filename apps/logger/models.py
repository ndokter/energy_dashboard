from django.db import connections, models
from django.db.models.aggregates import Sum
from django.utils.translation import ugettext as _


class PowerMeter(models.Model):
    UNIT_KWH = 'kwh'
    UNIT_M3 = 'm3'

    UNITS = (
        (UNIT_KWH, _('Kilowatt hour')),
        (UNIT_M3, _('Cubic meter'))
    )

    name = models.CharField(max_length=255)
    unit = models.CharField(choices=UNITS, max_length=10)


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


class Reading(models.Model):
    objects = ReadingReportsQuerySet.as_manager()

    power_meter = models.ForeignKey(
        'logger.PowerMeter',
        related_name='readings',
        db_index=True
    )
    datetime = models.DateTimeField(db_index=True)
    value_increment = models.FloatField()
    value_total = models.FloatField(db_index=True)

    class Meta:
        db_table = 'reading'

    def save(self, **kwargs):

        # Calculate the increment from the previous record.
        last_record = Reading.objects\
            .filter(power_meter=self.power_meter)\
            .order_by('datetime')\
            .last()

        if last_record:
            self.value_increment = \
                self.value_total - last_record.value_total
        else:
            self.value_increment = 0

        super(Reading, self).save(**kwargs)
