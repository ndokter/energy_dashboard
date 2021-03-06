# -*- coding: utf-8 -*-
# Generated by Django 1.9.12 on 2018-02-25 13:13
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('logger', '0018_auto_20180225_1305'),
    ]

    operations = [
        migrations.AlterField(
            model_name='metricactual',
            name='meter',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='metrics_actual', to='logger.Meter'),
        ),
        migrations.AlterField(
            model_name='metrictotal',
            name='meter_tariff',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='metrics_total', to='logger.MeterTariff'),
        ),
    ]
