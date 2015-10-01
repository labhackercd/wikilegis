# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='bill',
            name='editors',
            field=models.ManyToManyField(help_text='Any users in any of these groups will have permission to change this document.', to='auth.Group', verbose_name='editors', blank=True),
        ),
    ]
