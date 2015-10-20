# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


def publish_previous_bills(apps, schema_editor):
    Bill = apps.get_model("core", "Bill")
    Bill.objects.update(status='2')


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_genericdata'),
    ]

    operations = [
        migrations.AddField(
            model_name='bill',
            name='status',
            field=models.CharField(default='1', max_length=2, verbose_name='status', choices=[('1', 'Draft'), ('2', 'Published'), ('3', 'Closed')]),
        ),
        migrations.RunPython(publish_previous_bills),
    ]

