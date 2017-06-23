import django_filters

from rest_framework import filters

from apps.logger.models import ReadingActual
from apps.logger.models.reading_total import ReadingTotal


class ReadingFilter(filters.FilterSet):
    datetime_start = django_filters.DateTimeFilter(
        name='datetime',
        lookup_expr='gte'
    )
    datetime_end = django_filters.DateTimeFilter(
        name='datetime',
        lookup_expr='lt'
    )

    class Meta:
        model = ReadingTotal
        fields = ['datetime']


class ReadingActualFilter(filters.FilterSet):
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
        model = ReadingActual
        fields = ['datetime']
