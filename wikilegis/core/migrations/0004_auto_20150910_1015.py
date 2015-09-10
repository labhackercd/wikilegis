# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_bill_short_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bill',
            name='short_description',
            field=models.TextField(max_length=10, null=True),
        ),
    ]
