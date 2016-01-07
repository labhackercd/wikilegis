# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_auto_20151209_1616'),
    ]

    operations = [
        migrations.CreateModel(
            name='TypeSegment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200, verbose_name='name')),
                ('abbreviation', models.CharField(max_length=200, verbose_name='abbreviation')),
                ('editable', models.BooleanField(default='True', verbose_name='editable')),
            ],
            options={
                'verbose_name': 'type segment',
                'verbose_name_plural': 'types segment',
            },
        ),
        migrations.AddField(
            model_name='billsegment',
            name='number',
            field=models.CharField(max_length=200, null=True, verbose_name='number', blank=True),
        ),
        migrations.AddField(
            model_name='billsegment',
            name='parent',
            field=models.ForeignKey(verbose_name='segment parent', blank=True, to='core.BillSegment', null=True),
        ),
        migrations.AlterField(
            model_name='billsegment',
            name='type',
            field=models.ForeignKey(verbose_name='type', to='core.TypeSegment'),
        ),
    ]
