# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-09-15 15:08
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('logger', '0003_migrate_meter_slug_to_tariff'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Meter',
            new_name='MeterTariff',
        ),
    ]