# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0023_auto_20160831_1520'),
    ]

    operations = [
        migrations.AlterField(
            model_name='billsegment',
            name='type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, verbose_name='type', blank=True, to='core.TypeSegment', null=True),
        ),
    ]
