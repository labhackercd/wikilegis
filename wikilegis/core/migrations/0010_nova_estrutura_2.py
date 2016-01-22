# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


def create_types_default(apps, schema_editor):
    TypeSegment = apps.get_model("core", "TypeSegment")

    article = TypeSegment()
    article.id = 1
    article.name = 'Artigo'
    article.editable = True
    article.save()

    title = TypeSegment()
    title.id = 2
    title.name = 'Título'
    title.editable = False
    title.save()


def migrate_types(apps, schema_editor):
    BillSegment = apps.get_model("core", "BillSegment")

    for segment in BillSegment.objects.all():
        if segment.type == 'article':
            segment.new_type_id = 1
            segment.save()
        elif segment.type == 'title':
            segment.new_type_id = 2
            segment.save()


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0009_nova_estrutura_1'),
    ]

    operations = [
        # create two types default
        migrations.RunPython(
            create_types_default
        ),
        # migrate type to fk
        migrations.RunPython(
            migrate_types
        ),
    ]
