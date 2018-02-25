from django.db import models


class MeterManager(models.Manager):

    def electricity_used(self):
        return self.get_or_create(slug=Meter.SLUG_ELECTRICITY_USED)[0]

    def electricity_delivered(self):
        return self.get_or_create(slug=Meter.SLUG_ELECTRICITY_DELIVERED)[0]

    def gas_tariff(self):
        meter = self.get_or_create(slug=Meter.SLUG_GAS)[0]

        # Gas doesn't has only one tariff and therefor uses a fixed one.
        return meter.tariffs.get_or_create(tariff=1)[0]

    def electricity_used_tariff(self, tariff):
        meter = self.get_or_create(slug=Meter.SLUG_ELECTRICITY_USED)[0]

        return meter.tariffs.get_or_create(tariff=tariff)[0]

    def electricity_delivered_tariff(self, tariff):
        meter = self.get_or_create(slug=Meter.SLUG_ELECTRICITY_DELIVERED)[0]

        return meter.tariffs.get_or_create(tariff=tariff)[0]


class Meter(models.Model):
    objects = models.Manager()
    manager = MeterManager()

    SLUG_ELECTRICITY_USED = 'electricity-used'
    SLUG_ELECTRICITY_DELIVERED = 'electricity-delivered'
    SLUG_GAS = 'gas'

    SLUG_CHOICES = (
        (SLUG_ELECTRICITY_USED, SLUG_ELECTRICITY_USED),
        (SLUG_ELECTRICITY_DELIVERED, SLUG_ELECTRICITY_DELIVERED),
        (SLUG_GAS, SLUG_GAS),
    )

    slug = models.CharField(max_length=50, choices=SLUG_CHOICES, unique=True)

    def metrics_total(self):
        """
        A queryset for all meter metrics that belong to this meter group.
        """
        from apps.logger.models.metric_total import MetricTotal

        return MetricTotal.objects.filter(meter_tariff__meter__pk=self.pk)
