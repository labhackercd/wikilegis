# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.conf import settings


class Migration(migrations.Migration):

    replaces = [('notification', '0001_initial'), ('notification', '0002_historynotification_segment'), ('notification', '0003_auto_20151019_1046'), ('notification', '0004_auto_20160112_1100'), ('notification', '0005_newsletter')]

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0012_bill_theme'),
        ('core', '0003_genericdata'),
    ]

    operations = [
        migrations.CreateModel(
            name='HistoryNotification',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('hour', models.DateTimeField(default=datetime.datetime.now, verbose_name='hour')),
                ('amendment', models.ForeignKey(verbose_name='amendment', to='core.BillSegment')),
            ],
            options={
                'ordering': ('-hour',),
                'verbose_name': 'history notification',
                'verbose_name_plural': 'history notifications',
            },
        ),
        migrations.CreateModel(
            name='Newsletter',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='modified')),
                ('periodicity', models.CharField(default=b'daily', max_length=20, verbose_name='periodicity', choices=[(b'daily', 'Daily'), (b'weekly', 'Weekly')])),
                ('status', models.BooleanField(default=True)),
                ('bill', models.ForeignKey(verbose_name='bill', to='core.Bill')),
                ('user', models.ForeignKey(related_name='newsletters', verbose_name='user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Newsletter',
                'verbose_name_plural': 'Newsletters',
            },
        ),
        migrations.AlterUniqueTogether(
            name='newsletter',
            unique_together=set([('user', 'bill')]),
        ),
    ]
