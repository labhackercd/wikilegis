# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auth2', '0008_auto_20160901_1343'),
        ('core', '0024_auto_20160901_1401'),
    ]

    operations = [
        migrations.AddField(
            model_name='bill',
            name='authors',
            field=models.ManyToManyField(related_name='bill_owner', verbose_name='authors', to='auth2.Congressman', blank=True),
        ),
    ]
