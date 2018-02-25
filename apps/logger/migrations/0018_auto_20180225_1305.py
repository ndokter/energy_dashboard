# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('logger', '0017_auto_20180225_1124'),
    ]

    operations = [
        migrations.RenameModel('ReadingActual', 'MetricActual'),
        migrations.RenameModel('ReadingTotal', 'MetricTotal'),
    ]
