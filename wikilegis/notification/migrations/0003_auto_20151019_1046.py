# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_genericdata'),
        ('notification', '0002_historynotification_segment'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='historynotification',
            name='bill',
        ),
        migrations.RemoveField(
            model_name='historynotification',
            name='segment',
        ),
        migrations.AddField(
            model_name='historynotification',
            name='amendment',
            field=models.ForeignKey(default=None, verbose_name='amendment',
                                    to='core.CitizenAmendment'),
            preserve_default=False,
        ),
    ]
