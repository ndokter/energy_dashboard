from rest_framework import generics
from rest_framework.filters import OrderingFilter, DjangoFilterBackend

from apps.logger.api.filters import MetricFilter, MetricActualFilter
from apps.logger.api.serializers import MetricSerializer, \
    MetricActualSerializer
from apps.logger.models.meter import Meter


class ElectricityUsedView(generics.ListAPIView):
    serializer_class = MetricSerializer
    filter_class = MetricFilter
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    ordering_fields = ('datetime',)

    def get_queryset(self):
        meter = Meter.objects.get(slug=Meter.SLUG_ELECTRICITY_USED)

        return meter\
            .metrics_total()\
            .datetime_aggregate(self.kwargs['aggregate'])


class ElectricityDeliveredView(generics.ListAPIView):
    serializer_class = MetricSerializer
    filter_class = MetricFilter
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    ordering_fields = ('datetime',)

    def get_queryset(self):
        meter = Meter.objects.get(slug=Meter.SLUG_ELECTRICITY_DELIVERED)

        return meter\
            .metrics_total()\
            .datetime_aggregate(self.kwargs['aggregate'])


class ElectricityActualUsageView(generics.ListAPIView):
    serializer_class = MetricActualSerializer
    filter_class = MetricActualFilter
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    ordering_fields = ('datetime',)

    def get_queryset(self):
        meter = Meter.objects.get(slug=Meter.SLUG_ELECTRICITY_USED)

        return meter\
            .metrics_actual\
            .datetime_aggregate(self.kwargs['aggregate'])


class ElectricityActualDeliveryView(generics.ListAPIView):
    serializer_class = MetricActualSerializer
    filter_class = MetricActualFilter
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    ordering_fields = ('datetime',)

    def get_queryset(self):
        meter = Meter.objects.get(slug=Meter.SLUG_ELECTRICITY_DELIVERED)

        return meter\
            .metrics_actual\
            .datetime_aggregate(self.kwargs['aggregate'])


class GasUsedView(generics.ListAPIView):
    serializer_class = MetricSerializer
    filter_class = MetricFilter
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    ordering_fields = ('datetime',)

    def get_queryset(self):
        meter = Meter.objects.get(slug=Meter.SLUG_GAS)

        return meter\
            .metrics_total()\
            .datetime_aggregate(self.kwargs['aggregate'])
