# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


def publish_previous_bills(apps, schema_editor):
    Bill = apps.get_model("core", "Bill")
    Bill.objects.update(status='published')


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_updownvote'),
    ]

    operations = [
        migrations.AddField(
            model_name='bill',
            name='status',
            field=models.CharField(default='draft', max_length=20, verbose_name='status',
                                   choices=[('draft', 'Draft'), ('published', 'Published'), ('closed', 'Closed')]),
        ),
        migrations.RunPython(publish_previous_bills),
    ]

