from django.db import models


class DatetimeAggregateQuerySet(models.QuerySet):
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
            .order_by('datetime__aggregate')
