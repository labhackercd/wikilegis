# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations
from django.db import models


class Migration(migrations.Migration):

    dependencies = [
        ('notification', '0003_auto_20151019_1046'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historynotification',
            name='amendment',
            field=models.ForeignKey(verbose_name='amendment', to='core.BillSegment'),
        ),
    ]
