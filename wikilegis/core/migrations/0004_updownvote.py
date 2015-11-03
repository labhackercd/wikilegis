# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0003_genericdata'),
    ]

    operations = [
        migrations.CreateModel(
            name='UpDownVote',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('object_id', models.IntegerField()),
                ('model', models.CharField(max_length=20, choices=[('segment', 'Segment'), ('amendment', 'Amendment')])),
                ('vote', models.CharField(max_length=10, choices=[('up', 'Up vote'), ('down', 'Down vote')])),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='created')),
                ('user', models.ForeignKey(verbose_name='user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
