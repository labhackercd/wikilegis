# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0018_auto_20160830_1526'),
    ]

    operations = [
        migrations.CreateModel(
            name='Theme',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='modified')),
                ('name', models.CharField(max_length=200, verbose_name='name')),
            ],
            options={
                'verbose_name': 'theme',
                'verbose_name_plural': 'Themes',
            },
        ),
        migrations.AddField(
            model_name='typesegment',
            name='apresentation_name',
            field=models.CharField(max_length=200, null=True, verbose_name='apresentation name', blank=True),
        ),
        migrations.AlterField(
            model_name='bill',
            name='theme',
            field=models.ForeignKey(verbose_name='theme', blank=True, to='core.Theme', null=True),
        ),
        migrations.AlterField(
            model_name='billsegment',
            name='number',
            field=models.CharField(max_length=200, null=True, verbose_name='number', blank=True),
        ),
    ]
