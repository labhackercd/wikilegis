# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_auto_20160111_1133'),
    ]

    operations = [
        migrations.AlterField(
            model_name='billsegment',
            name='number',
            field=models.PositiveIntegerField(default=0, null=True, verbose_name='number', blank=True),
        ),
    ]
