# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0016_auto_20160706_1619'),
    ]

    operations = [
        migrations.AlterField(
            model_name='updownvote',
            name='vote',
            field=models.BooleanField(default=False, choices=[(True, 'Up Vote'), (False, 'Down Vote')]),
        ),
    ]
