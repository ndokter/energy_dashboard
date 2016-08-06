import django_filters

from rest_framework import filters
from rest_framework import generics
from rest_framework.generics import get_object_or_404

from apps.logger.api.serializers import ReadingReportSerializer
from apps.logger.models import Meter, Reading


class ReadingReportFilter(filters.FilterSet):
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


class ReadingReportView(generics.ListAPIView):
    serializer_class = ReadingReportSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_class = ReadingReportFilter

    def get_queryset(self):
        meter = get_object_or_404(Meter, code=self.kwargs['meter_code'])

        return meter.readings.datetime_aggregate(self.kwargs['aggregate'])
