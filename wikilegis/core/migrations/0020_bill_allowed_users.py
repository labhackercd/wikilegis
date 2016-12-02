# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0019_auto_20160928_1517'),
    ]

    operations = [
        migrations.AddField(
            model_name='bill',
            name='allowed_users',
            field=models.ManyToManyField(related_name='allowed', verbose_name='allowed users', to=settings.AUTH_USER_MODEL, blank=True),
        ),
    ]
