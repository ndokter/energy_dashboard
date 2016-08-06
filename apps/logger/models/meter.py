from django.db import models
from django.utils.translation import ugettext as _


class Meter(models.Model):
    UNIT_KWH = 'kwh'
    UNIT_M3 = 'm3'

    UNITS = (
        (UNIT_KWH, _('Kilowatt hour')),
        (UNIT_M3, _('Cubic meter'))
    )

    code = models.CharField(max_length=50, unique=True)
    display_name = models.CharField(max_length=255, null=True, blank=True)
    unit = models.CharField(choices=UNITS, max_length=10)

    @staticmethod
    def get_electricity_used_meter(tariff):
        return Meter.objects.get_or_create(
            name='electricity_used_t{}'.format(tariff),
            unit=Meter.UNIT_KWH
        )[0]

    @staticmethod
    def get_electricity_delivered_meter(tariff):
        return Meter.objects.get_or_create(
            name='electricity_delivered_t{}'.format(tariff),
            unit=Meter.UNIT_KWH
        )[0]

    @staticmethod
    def get_gas_meter():
        return Meter.objects.get_or_create(
            name='gas',
            unit=Meter.UNIT_M3
        )[0]
