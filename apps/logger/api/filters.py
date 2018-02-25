import django_filters

from rest_framework import filters

from apps.logger.models import MetricActual
from apps.logger.models.metric_total import MetricTotal


class MetricFilter(filters.FilterSet):
    datetime_start = django_filters.DateTimeFilter(
        name='datetime',
        lookup_expr='gte'
    )
    datetime_end = django_filters.DateTimeFilter(
        name='datetime',
        lookup_expr='lt'
    )

    class Meta:
        model = MetricTotal
        fields = ['datetime']


class MetricActualFilter(filters.FilterSet):
    datetime_start = django_filters.DateTimeFilter(
        name='datetime',
        lookup_expr='gte'
    )
    datetime_end = django_filters.DateTimeFilter(
        name='datetime',
        lookup_expr='lt'
    )
    aggregation = django_filters.ChoiceFilter()

    class Meta:
        model = MetricActual
        fields = ['datetime']
