from django.db import models

from apps.logger.models.meter import Meter


class MeterTariff(models.Model):
    UNIT_KWH = 'kWh'
    UNIT_M3 = 'm3'

    UNIT_CHOICES = (
        (UNIT_KWH, UNIT_KWH),
        (UNIT_M3, UNIT_M3),
    )

    meter = models.ForeignKey(Meter, related_name='tariffs')

    tariff = models.PositiveSmallIntegerField()
    unit = models.CharField(max_length=10, choices=UNIT_CHOICES)
