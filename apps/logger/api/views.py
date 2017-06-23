from rest_framework import generics
from rest_framework.filters import OrderingFilter, DjangoFilterBackend

from apps.logger.api.filters import ReadingFilter, ReadingActualFilter
from apps.logger.api.serializers import ReadingSerializer, \
    ReadingActualSerializer
from apps.logger.models.meter import Meter


class ReadingElectricityUsedView(generics.ListAPIView):
    serializer_class = ReadingSerializer
    filter_class = ReadingFilter
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    ordering_fields = ('datetime',)

    def get_queryset(self):
        meter = Meter.objects.get(slug=Meter.SLUG_ELECTRICITY_USED)

        return meter\
            .readings_total()\
            .datetime_aggregate(self.kwargs['aggregate'])


class ReadingElectricityDeliveredView(generics.ListAPIView):
    serializer_class = ReadingSerializer
    filter_class = ReadingFilter
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    ordering_fields = ('datetime',)

    def get_queryset(self):
        meter = Meter.objects.get(slug=Meter.SLUG_ELECTRICITY_DELIVERED)

        return meter\
            .readings_total()\
            .datetime_aggregate(self.kwargs['aggregate'])


class ElectricityActualUsageView(generics.ListAPIView):
    serializer_class = ReadingActualSerializer
    filter_class = ReadingActualFilter
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    ordering_fields = ('datetime',)

    def get_queryset(self):
        meter = Meter.objects.get(slug=Meter.SLUG_ELECTRICITY_USED)

        return meter\
            .readings_actual\
            .datetime_aggregate(self.kwargs['aggregate'])


class ElectricityActualDeliveryView(generics.ListAPIView):
    serializer_class = ReadingActualSerializer
    filter_class = ReadingActualFilter
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    ordering_fields = ('datetime',)

    def get_queryset(self):
        meter = Meter.objects.get(slug=Meter.SLUG_ELECTRICITY_DELIVERED)

        return meter\
            .readings_actual\
            .datetime_aggregate(self.kwargs['aggregate'])


class ReadingGasUsedView(generics.ListAPIView):
    serializer_class = ReadingSerializer
    filter_class = ReadingFilter
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    ordering_fields = ('datetime',)

    def get_queryset(self):
        meter = Meter.objects.get(slug=Meter.SLUG_GAS)

        return meter\
            .readings_total()\
            .datetime_aggregate(self.kwargs['aggregate'])
