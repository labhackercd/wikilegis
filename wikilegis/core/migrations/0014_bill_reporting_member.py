# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0013_auto_20160512_1753'),
    ]

    operations = [
        migrations.AddField(
            model_name='bill',
            name='reporting_member',
            field=models.ForeignKey(verbose_name='reporting member', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
    ]
