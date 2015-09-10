# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_remove_bill_short_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='bill',
            name='short_description',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
