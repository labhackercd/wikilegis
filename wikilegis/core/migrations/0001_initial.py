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
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('short_description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='BillSegment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('order', models.PositiveIntegerField(default=0)),
                ('content', models.TextField()),
                ('type', models.CharField(max_length=64, choices=[(b'title', 'Title'), (b'article', 'Article')])),
                ('bill', models.ForeignKey(related_name='segments', verbose_name=b'Bill', to='core.Bill')),
            ],
            options={
                'ordering': ('order',),
            },
        ),
        migrations.CreateModel(
            name='CitizenAmendment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('content', models.TextField()),
                ('comment', models.TextField(null=True, blank=True)),
                ('author', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('segment', models.ForeignKey(related_name='amendments', verbose_name=b'BillSegment', to='core.BillSegment')),
            ],
        ),
        migrations.CreateModel(
            name='UserSegmentChoice',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('amendment', models.ForeignKey(related_name='choosings', verbose_name=b'choosings', blank=True, to='core.CitizenAmendment', null=True)),
                ('segment', models.ForeignKey(related_name='choices', verbose_name=b'choices', to='core.BillSegment')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
