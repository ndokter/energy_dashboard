from rest_framework import generics

from apps.logger.api.filters import ElectricityReadingFilter, ReadingFilter
from apps.logger.api.serializers import ElectricityReadingSerializer, \
    ReadingSerializer
from apps.logger.models.reading import ElectricityUsedReading, GasUsedReading, \
    ElectricityDeliveredReading


class ReadingElectricityUsedView(generics.ListAPIView):
    serializer_class = ElectricityReadingSerializer
    filter_class = ElectricityReadingFilter

    def get_queryset(self):
        return ElectricityUsedReading.objects\
            .datetime_aggregate(self.kwargs['aggregate'])


class ReadingElectricityDeliveredView(generics.ListAPIView):
    serializer_class = ElectricityReadingSerializer
    filter_class = ElectricityReadingFilter

    def get_queryset(self):
        return ElectricityDeliveredReading.objects\
            .datetime_aggregate(self.kwargs['aggregate'])


class ReadingGasUsedView(generics.ListAPIView):
    serializer_class = ReadingSerializer
    filter_class = ReadingFilter

    def get_queryset(self):
        return GasUsedReading.objects\
            .datetime_aggregate(self.kwargs['aggregate'])
