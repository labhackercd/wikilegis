# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import image_cropping.fields


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0021_auto_20160831_1104'),
    ]

    operations = [
        migrations.AlterField(
            model_name='theme',
            name=b'cropping',
            field=image_cropping.fields.ImageRatioField('icon', '50x50', hide_image_field=False, size_warning=False, allow_fullsize=False, free_crop=False, adapt_rotation=False, help_text='Note that the preview above will only be updated after you submit the form.', verbose_name='cropping'),
        ),
    ]
