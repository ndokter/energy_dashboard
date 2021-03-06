# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-08-21 10:19
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Meter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.CharField(max_length=50)),
                ('unit', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='MeterGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.CharField(max_length=50, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='MeterPrice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start', models.DateField()),
                ('end', models.DateField()),
                ('amount', models.DecimalField(decimal_places=4, max_digits=4)),
                ('meter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='prices', to='logger.Meter')),
            ],
        ),
        migrations.CreateModel(
            name='Reading',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime', models.DateTimeField()),
                ('value_increment', models.DecimalField(decimal_places=3, max_digits=8)),
                ('value_total', models.DecimalField(decimal_places=3, max_digits=9)),
                ('costs', models.DecimalField(decimal_places=4, max_digits=9, null=True)),
                ('meter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='readings', to='logger.Meter')),
            ],
            options={
                'ordering': ['datetime'],
            },
        ),
        migrations.AddField(
            model_name='meter',
            name='meter_group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='meters', to='logger.MeterGroup'),
        ),
        migrations.AlterIndexTogether(
            name='reading',
            index_together=set([('meter', 'datetime')]),
        ),
    ]
