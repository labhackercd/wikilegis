# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0010_nova_estrutura_2'),
    ]

    operations = [
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
