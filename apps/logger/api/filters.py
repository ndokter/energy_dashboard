import django_filters

from rest_framework import filters

from apps.logger.models.reading import AbstractReading


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
        model = AbstractReading
        fields = ['datetime']


class ElectricityReadingFilter(ReadingFilter):
    tariff = django_filters.NumberFilter()
