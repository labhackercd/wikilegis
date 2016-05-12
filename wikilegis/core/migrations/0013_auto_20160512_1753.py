# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_bill_theme'),
    ]

    operations = [
        migrations.AddField(
            model_name='bill',
            name='epigraph',
            field=models.CharField(max_length=255, null=True, verbose_name='epigraph'),
        ),
        migrations.AlterField(
            model_name='bill',
            name='description',
            field=models.TextField(verbose_name='digest'),
        ),
        migrations.AlterField(
            model_name='bill',
            name='title',
            field=models.CharField(max_length=255, verbose_name='subject'),
        ),
    ]
