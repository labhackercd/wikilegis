# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_auto_20150910_1015'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bill',
            name='short_description',
            field=models.TextField(max_length=300, null=True),
        ),
    ]
