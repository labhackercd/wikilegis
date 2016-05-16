# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations
from django.db import models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_auto_20151110_1304'),
    ]

    operations = [
        migrations.AlterField(
            model_name='proposition',
            name='appraisal',
            field=models.TextField(null=True, verbose_name='appraisal', blank=True),
        ),
        migrations.AlterField(
            model_name='proposition',
            name='indexing',
            field=models.TextField(null=True, verbose_name='indexing', blank=True),
        ),
    ]
