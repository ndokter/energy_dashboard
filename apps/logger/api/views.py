import datetime

from django.utils import timezone
from rest_framework import generics

from apps.logger.api.filters import ReadingFilter
from apps.logger.api.serializers import ReadingSerializer
from apps.logger.models.meter import MeterGroup


class ReadingElectricityUsedView(generics.ListAPIView):
    serializer_class = ReadingSerializer
    filter_class = ReadingFilter

    def get_queryset(self):
        meter_group = MeterGroup.objects.get(
            slug=MeterGroup.SLUG_ELECTRICITY_USED
        )

        return meter_group\
            .readings()\
            .datetime_aggregate(self.kwargs['aggregate'])


class ReadingElectricityDeliveredView(generics.ListAPIView):
    serializer_class = ReadingSerializer
    filter_class = ReadingFilter

    def get_queryset(self):
        meter_group = MeterGroup.objects.get(
            slug=MeterGroup.SLUG_ELECTRICITY_DELIVERED
        )

        return meter_group\
            .readings()\
            .datetime_aggregate(self.kwargs['aggregate'])


class ReadingGasUsedView(generics.ListAPIView):
    serializer_class = ReadingSerializer
    filter_class = ReadingFilter

    def get_queryset(self):
        meter_group = MeterGroup.objects.get(
            slug=MeterGroup.SLUG_GAS
        )

        return meter_group\
            .readings()\
            .datetime_aggregate(self.kwargs['aggregate'])
