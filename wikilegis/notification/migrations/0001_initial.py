# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import datetime
from django.db import migrations
from django.db import models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_genericdata'),
    ]

    operations = [
        migrations.CreateModel(
            name='HistoryNotification',
            fields=[
                ('id', models.AutoField(verbose_name='ID',
                                        serialize=False, auto_created=True, primary_key=True)),
                ('hour', models.DateTimeField(default=datetime.datetime.now, verbose_name='hour')),
                ('bill', models.ForeignKey(verbose_name='bill', to='core.Bill')),
            ],
            options={
                'ordering': ('-hour',),
                'verbose_name': 'history notification',
                'verbose_name_plural': 'history notifications',
            },
        ),
    ]
