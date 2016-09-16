from django.db import models

from apps.logger.models.meter_tariff import MeterTariff


class MeterTariffPriceQuerySet(models.QuerySet):

    def active(self, datetime):
        """
        Get active price for the given datetime.
        """
        try:
            return self.filter(start__lte=datetime, end__gt=datetime).get()
        except MeterTariffPrice.DoesNotExist:
            return


class MeterTariffPrice(models.Model):
    objects = MeterTariffPriceQuerySet.as_manager()

    meter_tariff = models.ForeignKey(MeterTariff, related_name='prices')

    start = models.DateField()
    end = models.DateField()
    amount = models.DecimalField(max_digits=4, decimal_places=4)
