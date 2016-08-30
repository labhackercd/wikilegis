# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0017_auto_20160808_1552'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='proposition',
            name='bill',
        ),
        migrations.AlterField(
            model_name='bill',
            name='reporting_member',
            field=models.ForeignKey(verbose_name='reporting member', blank=True, to='auth2.Congressman', null=True),
        ),
        migrations.DeleteModel(
            name='Proposition',
        ),
    ]
