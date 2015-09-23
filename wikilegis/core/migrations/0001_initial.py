# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Bill',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='modified')),
                ('title', models.CharField(max_length=255, verbose_name='title')),
                ('description', models.TextField(verbose_name='description')),
            ],
            options={
                'verbose_name': 'bill',
                'verbose_name_plural': 'bills',
            },
        ),
        migrations.CreateModel(
            name='BillSegment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='modified')),
                ('order', models.PositiveIntegerField(default=0, verbose_name='order')),
                ('content', models.TextField(verbose_name='content')),
                ('type', models.CharField(max_length=64, verbose_name='type', choices=[('title', 'Title'), ('article', 'Article')])),
                ('bill', models.ForeignKey(related_name='segments', verbose_name='bill', to='core.Bill')),
            ],
            options={
                'ordering': ('order',),
                'verbose_name': 'segment',
                'verbose_name_plural': 'segments',
            },
        ),
        migrations.CreateModel(
            name='CitizenAmendment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='modified')),
                ('content', models.TextField(verbose_name='content')),
                ('author', models.ForeignKey(verbose_name='author', to=settings.AUTH_USER_MODEL)),
                ('segment', models.ForeignKey(related_name='amendments', verbose_name='bill segment', to='core.BillSegment')),
            ],
            options={
                'verbose_name': 'citizen amendment',
                'verbose_name_plural': 'citizen amendments',
            },
        ),
        migrations.CreateModel(
            name='UserSegmentChoice',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('amendment', models.ForeignKey(related_name='choosings', verbose_name='amendment', blank=True, to='core.CitizenAmendment', null=True)),
                ('segment', models.ForeignKey(related_name='choices', verbose_name='bill segment', to='core.BillSegment')),
                ('user', models.ForeignKey(verbose_name='user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='usersegmentchoice',
            unique_together=set([('user', 'segment')]),
        ),
    ]
