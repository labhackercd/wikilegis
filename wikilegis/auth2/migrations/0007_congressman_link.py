# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auth2', '0006_auto_20160830_1526'),
    ]

    operations = [
        migrations.AddField(
            model_name='congressman',
            name='link',
            field=models.URLField(null=True, verbose_name='parliamentary link', blank=True),
        ),
    ]
