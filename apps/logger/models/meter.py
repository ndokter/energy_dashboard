from django.db import models


class MeterManager(models.Manager):

    def electricity_used(self, tariff):
        meter_group = self.get_or_create(
            slug=MeterGroup.SLUG_ELECTRICITY_USED
        )[0]

        return meter_group.meters.get_or_create(
            slug='t{}'.format(tariff)
        )[0]

    def electricity_delivered(self, tariff):
        meter_group = self.get_or_create(
            slug=MeterGroup.SLUG_ELECTRICITY_DELIVERED
        )[0]

        return meter_group.meters.get_or_create(
            slug='t{}'.format(tariff)
        )[0]

    def gas(self):
        meter_group = self.get_or_create(slug=MeterGroup.SLUG_GAS)[0]

        return meter_group.meters.get_or_create(slug='gas')[0]


class MeterGroup(models.Model):
    objects = models.Manager()
    meter = MeterManager()

    SLUG_ELECTRICITY_USED = 'electricity-used'
    SLUG_ELECTRICITY_DELIVERED = 'electricity-delivered'
    SLUG_GAS = 'gas'

    slug = models.CharField(max_length=50, unique=True)

    def readings(self):
        """
        A queryset for all meter readings that belong to this meter group.
        """
        from apps.logger.models.reading import Reading

        return Reading.objects.filter(meter__in=self.meters.all())


class Meter(models.Model):
    UNIT_KWH = 'kWh'
    UNIT_M3 = 'm3'

    meter_group = models.ForeignKey(MeterGroup, related_name='meters')

    slug = models.CharField(max_length=50)
    unit = models.CharField(max_length=10)


class MeterPriceQuerySet(models.QuerySet):
    def active(self, datetime):
        """
        Get active price for the given datetime.
        """
        try:
            return self.filter(start__lte=datetime, end__gt=datetime).get()
        except MeterPrice.DoesNotExist:
            return


class MeterPrice(models.Model):
    objects = MeterPriceQuerySet.as_manager()

    meter = models.ForeignKey(Meter, related_name='prices')

    start = models.DateField()
    end = models.DateField()
    amount = models.DecimalField(max_digits=4, decimal_places=4)
