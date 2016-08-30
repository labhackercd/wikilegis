# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0019_auto_20160830_1545'),
    ]

    operations = [
        migrations.AlterField(
            model_name='billsegment',
            name='type',
            field=models.ForeignKey(verbose_name='type', blank=True, to='core.TypeSegment', null=True),
        ),
    ]
