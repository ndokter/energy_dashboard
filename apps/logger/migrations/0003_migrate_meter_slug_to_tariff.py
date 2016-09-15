from __future__ import unicode_literals

from django.db import migrations


def forwards(apps, schema_editor):
    Meter = apps.get_model('logger', 'Meter')

    Meter.objects.filter(slug='t1').update(tariff=1)
    Meter.objects.filter(slug='t2').update(tariff=2)
    Meter.objects.filter(slug='gas').update(tariff=1)


class Migration(migrations.Migration):

    dependencies = [
        ('logger', '0002_meter_tariff'),
    ]

    operations = [
        migrations.RunPython(forwards),
    ]
