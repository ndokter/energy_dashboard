from rest_framework import generics

from apps.logger.api.filters import ReadingFilter, EnergyActualFilter
from apps.logger.api.serializers import ReadingSerializer, \
    EnergyActualSerializer
from apps.logger.models.meter import Meter


class ReadingElectricityUsedView(generics.ListAPIView):
    serializer_class = ReadingSerializer
    filter_class = ReadingFilter

    def get_queryset(self):
        meter = Meter.objects.get(slug=Meter.SLUG_ELECTRICITY_USED)

        return meter\
            .readings()\
            .datetime_aggregate(self.kwargs['aggregate'])


class ReadingElectricityDeliveredView(generics.ListAPIView):
    serializer_class = ReadingSerializer
    filter_class = ReadingFilter

    def get_queryset(self):
        meter = Meter.objects.get(slug=Meter.SLUG_ELECTRICITY_DELIVERED)

        return meter\
            .readings()\
            .datetime_aggregate(self.kwargs['aggregate'])


class ElectricityActualUsageView(generics.ListAPIView):
    serializer_class = EnergyActualSerializer
    filter_class = EnergyActualFilter

    def get_queryset(self):
        meter = Meter.objects.get(slug=Meter.SLUG_ELECTRICITY_USED)

        return meter\
            .energy_actual\
            .datetime_aggregate(self.kwargs['aggregate'])


class ElectricityActualDeliveryView(generics.ListAPIView):
    serializer_class = EnergyActualSerializer
    filter_class = EnergyActualFilter

    def get_queryset(self):
        meter = Meter.objects.get(slug=Meter.SLUG_ELECTRICITY_DELIVERED)

        return meter\
            .energy_actual\
            .datetime_aggregate(self.kwargs['aggregate'])


class ReadingGasUsedView(generics.ListAPIView):
    serializer_class = ReadingSerializer
    filter_class = ReadingFilter

    def get_queryset(self):
        meter = Meter.objects.get(slug=Meter.SLUG_GAS)

        return meter\
            .readings()\
            .datetime_aggregate(self.kwargs['aggregate'])
