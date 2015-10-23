# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_proposition'),
    ]

    operations = [
        migrations.AlterField(
            model_name='proposition',
            name='menu',
            field=models.TextField(null=True, verbose_name='menu', blank=True),
        ),
    ]
