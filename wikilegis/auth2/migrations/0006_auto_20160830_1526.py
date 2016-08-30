# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auth2', '0005_congressman'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='id_congressman',
        ),
        migrations.AddField(
            model_name='user',
            name='is_congressman',
            field=models.BooleanField(default=False, verbose_name='Is Congressman'),
        ),
    ]
