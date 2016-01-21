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
    title.name = 2
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
        ('core', '0008_auto_20151209_1616'),
    ]

    operations = [
        migrations.CreateModel(
            name='TypeSegment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200, verbose_name='name')),
                ('editable', models.BooleanField(default='True', verbose_name='editable')),
            ],
            options={
                'verbose_name': 'type segment',
                'verbose_name_plural': 'types segment',
            },
        ),
        # create two types default
        migrations.RunPython(
            create_types_default
        ),
        migrations.AddField(
            model_name='billsegment',
            name='author',
            field=models.ForeignKey(verbose_name='author', to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='billsegment',
            name='number',
            field=models.PositiveIntegerField(null=True, verbose_name='number', blank=True),
        ),
        migrations.AddField(
            model_name='billsegment',
            name='original',
            field=models.BooleanField(default=True, verbose_name='original'),
        ),
        migrations.AddField(
            model_name='billsegment',
            name='parent',
            field=models.ForeignKey(related_name='children', verbose_name='segment parent', blank=True, to='core.BillSegment', null=True),
        ),
        migrations.AddField(
            model_name='billsegment',
            name='replaced',
            field=models.ForeignKey(related_name='substitutes', verbose_name='segment replaced', blank=True, to='core.BillSegment', null=True),
        ),
        migrations.AddField(
            model_name='billsegment',
            name='new_type',
            field=models.ForeignKey(verbose_name='type', to='core.TypeSegment', blank=True, null=True),
        ),
        # migrate type to fk
        migrations.RunPython(
            migrate_types
        ),
        migrations.RemoveField(
            model_name='billsegment',
            name='type'
        ),
        migrations.AlterField(
            model_name='billsegment',
            name='new_type',
            field=models.ForeignKey(verbose_name='type', to='core.TypeSegment'),
        ),
        migrations.RenameField(
            model_name='billsegment',
            old_name='new_type',
            new_name='type',
        ),
    ]
