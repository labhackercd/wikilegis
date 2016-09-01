# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auth2', '0007_congressman_link'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='is_congressman',
        ),
        migrations.AlterField(
            model_name='congressman',
            name='link',
            field=models.URLField(null=True, verbose_name='parliamentary website', blank=True),
        ),
    ]
