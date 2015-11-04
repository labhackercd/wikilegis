# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.contenttypes.models import ContentType

from django.db import models, migrations
from django.conf import settings
from wikilegis.core.models import CitizenAmendment, UserSegmentChoice, BillSegment


def combine_votes(apps, schema_editor):
    UpDownVote = apps.get_model("core", "UpDownVote")
    for segmentChoice in UserSegmentChoice.objects.all():
        if segmentChoice.amendment_id:
            UpDownVote.objects.create(user_id=segmentChoice.user_id, object_id=segmentChoice.amendment_id, vote=1,
                                      content_type_id=ContentType.objects.get_for_model(CitizenAmendment).id)
        else:
            UpDownVote.objects.create(user_id=segmentChoice.user_id, object_id=segmentChoice.segment_id, vote=1,
                                      content_type_id=ContentType.objects.get_for_model(BillSegment).id)


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0003_genericdata'),
    ]

    operations = [
        migrations.CreateModel(
            name='UpDownVote',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='modified')),
                ('object_id', models.PositiveIntegerField()),
                ('vote', models.BooleanField(choices=[(True, 'Up Vote'), (False, 'Down Vote')])),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType')),
                ('user', models.ForeignKey(verbose_name='user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='updownvote',
            unique_together=set([('user', 'object_id', 'content_type')]),
        ),
        migrations.RunPython(combine_votes),
    ]
