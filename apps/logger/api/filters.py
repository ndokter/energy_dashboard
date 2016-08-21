import django_filters

from rest_framework import filters

from apps.logger.models.reading import Reading


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
        model = Reading
        fields = ['datetime']
