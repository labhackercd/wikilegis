# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0018_auto_20160919_1331'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bill',
            name='closing_date',
            field=models.DateField(default=datetime.datetime(2016, 12, 31, 0, 0), verbose_name='closing date'),
            preserve_default=False,
        ),
    ]
