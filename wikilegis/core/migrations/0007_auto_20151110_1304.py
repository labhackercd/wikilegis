# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_proposition'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bill',
            name='status',
            field=models.CharField(default='1', max_length=20, verbose_name=
                                   'status', choices=[('draft', 'Draft'),
                                                      ('published', 'Published'),
                                                      ('closed', 'Closed')]),
        ),
    ]
