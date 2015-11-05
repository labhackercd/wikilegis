# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_genericdata'),
        ('notification', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='historynotification',
            name='segment',
            field=models.ForeignKey(default=None, verbose_name='segment', to='core.BillSegment'),
            preserve_default=False,
        ),
    ]
