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

        # TODO tmp (move the range responsibility to the front-end)
        end = timezone.now()
        start = end - datetime.timedelta(days=1)

        return meter_group\
            .readings()\
            .filter(datetime__range=[start, end])\
            .datetime_aggregate(self.kwargs['aggregate'])


class ReadingElectricityDeliveredView(generics.ListAPIView):
    serializer_class = ReadingSerializer
    filter_class = ReadingFilter

    def get_queryset(self):
        meter_group = MeterGroup.objects.get(
            slug=MeterGroup.SLUG_ELECTRICITY_DELIVERED
        )

        # TODO tmp (move the range responsibility to the front-end)
        end = timezone.now()
        start = end - datetime.timedelta(days=1)

        return meter_group\
            .readings()\
            .filter(datetime__range=[start, end])\
            .datetime_aggregate(self.kwargs['aggregate'])


class ReadingGasUsedView(generics.ListAPIView):
    serializer_class = ReadingSerializer
    filter_class = ReadingFilter

    def get_queryset(self):
        meter_group = MeterGroup.objects.get(
            slug=MeterGroup.SLUG_GAS
        )

        # TODO tmp (move the range responsibility to the front-end)
        end = timezone.now()
        start = end - datetime.timedelta(days=1)

        return meter_group\
            .readings()\
            .filter(datetime__gte=start, datetime__lt=end)\
            .datetime_aggregate(self.kwargs['aggregate'])
