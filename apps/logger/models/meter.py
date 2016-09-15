from django.db import models


class MeterManager(models.Manager):

    def electricity_used(self, tariff):
        meter, _ = self.get_or_create(slug=Meter.SLUG_ELECTRICITY_USED)

        return meter.tariffs.get_or_create(tariff=tariff)[0]

    def electricity_delivered(self, tariff):
        meter, _ = self.get_or_create(slug=Meter.SLUG_ELECTRICITY_DELIVERED)

        return meter.tariffs.get_or_create(tariff=tariff)[0]

    def gas(self):
        meter, _ = self.get_or_create(slug=Meter.SLUG_GAS)

        # Gas doesn't has only one tariff and therefor uses a fixed one.
        return meter.tariffs.get_or_create(tariff=1)[0]


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

    def readings(self):
        """
        A queryset for all meter readings that belong to this meter group.
        """
        from apps.logger.models.reading import Reading

        return Reading.objects.filter(meter_tariff__meter__pk=self.pk)


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


class MeterPriceQuerySet(models.QuerySet):

    def active(self, datetime):
        """
        Get active price for the given datetime.
        """
        try:
            return self.filter(start__lte=datetime, end__gt=datetime).get()
        except MeterTariffPrice.DoesNotExist:
            return


class MeterTariffPrice(models.Model):
    objects = MeterPriceQuerySet.as_manager()

    meter_tariff = models.ForeignKey(MeterTariff, related_name='prices')

    start = models.DateField()
    end = models.DateField()
    amount = models.DecimalField(max_digits=4, decimal_places=4)
