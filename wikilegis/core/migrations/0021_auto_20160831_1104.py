# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import image_cropping.fields
import wikilegis.auth2.models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0020_auto_20160830_1637'),
    ]

    operations = [
        migrations.AddField(
            model_name='theme',
            name=b'cropping',
            field=image_cropping.fields.ImageRatioField('avatar', '50x50', hide_image_field=False, size_warning=False, allow_fullsize=False, free_crop=False, adapt_rotation=False, help_text='Note that the preview above will only be updated after you submit the form.', verbose_name='cropping'),
        ),
        migrations.AddField(
            model_name='theme',
            name='icon',
            field=image_cropping.fields.ImageCropField(blank=True, upload_to='icons/', null=True, verbose_name='icon', validators=[wikilegis.auth2.models.avatar_validation]),
        ),
    ]
