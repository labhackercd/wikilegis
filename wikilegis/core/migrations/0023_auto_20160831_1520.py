# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
import image_cropping.fields
import wikilegis.auth2.models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0022_auto_20160831_1156'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bill',
            name='theme',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, verbose_name='theme', blank=True, to='core.Theme', null=True),
        ),
        migrations.AlterField(
            model_name='theme',
            name='icon',
            field=image_cropping.fields.ImageCropField(default=None, upload_to='icons/', verbose_name='icon', validators=[wikilegis.auth2.models.avatar_validation]),
            preserve_default=False,
        ),
    ]
