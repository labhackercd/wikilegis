# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0009_auto_20160106_1426'),
    ]

    operations = [
        migrations.AddField(
            model_name='billsegment',
            name='author',
            field=models.ForeignKey(verbose_name='author', to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='billsegment',
            name='original',
            field=models.BooleanField(default=True, verbose_name='original'),
        ),
        migrations.AddField(
            model_name='billsegment',
            name='replaced',
            field=models.ForeignKey(related_name='substitutes', verbose_name='segment replaced', blank=True, to='core.BillSegment', null=True),
        ),
        migrations.AlterField(
            model_name='billsegment',
            name='parent',
            field=models.ForeignKey(related_name='children', verbose_name='segment parent', blank=True, to='core.BillSegment', null=True),
        ),
        migrations.AlterField(
            model_name='typesegment',
            name='abbreviation',
            field=models.CharField(max_length=200, null=True, verbose_name='abbreviation', blank=True),
        ),
    ]
