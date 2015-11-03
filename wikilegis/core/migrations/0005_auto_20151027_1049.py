# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_updownvote'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='updownvote',
            name='model',
        ),
        migrations.AddField(
            model_name='updownvote',
            name='amendment',
            field=models.ForeignKey(related_name='votes_amendment', verbose_name='amendment', blank=True, to='core.CitizenAmendment', null=True),
        ),
        migrations.AddField(
            model_name='updownvote',
            name='segment',
            field=models.ForeignKey(related_name='votes_segment', verbose_name='bill segment', blank=True, to='core.BillSegment', null=True),
        ),
    ]
