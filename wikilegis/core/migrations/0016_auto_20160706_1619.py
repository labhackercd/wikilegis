# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0015_auto_20160627_1532'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='citizenamendment',
            name='author',
        ),
        migrations.RemoveField(
            model_name='citizenamendment',
            name='segment',
        ),
        migrations.AlterField(
            model_name='bill',
            name='closing_date',
            field=models.DateField(null=True, verbose_name='closing date', blank=True),
        ),
        migrations.DeleteModel(
            name='CitizenAmendment',
        ),
    ]
