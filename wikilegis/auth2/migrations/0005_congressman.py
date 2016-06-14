# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('auth2', '0004_auto_20151113_1552'),
    ]

    operations = [
        migrations.CreateModel(
            name='Congressman',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('uf', models.CharField(max_length=200, null=True, verbose_name='uf', blank=True)),
                ('party', models.CharField(max_length=200, null=True, verbose_name='party', blank=True)),
                ('parliamentary_name', models.CharField(max_length=200, null=True, verbose_name='parliamentary name', blank=True)),
                ('user', models.ForeignKey(verbose_name='user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'congressman',
                'verbose_name_plural': 'congressmen',
            },
        ),
    ]
