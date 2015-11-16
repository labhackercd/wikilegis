# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import image_cropping.fields
import wikilegis.auth2.models


class Migration(migrations.Migration):

    dependencies = [
        ('auth2', '0002_add_user_avatar'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='id_congressman',
            field=models.CharField(help_text='The id of each congressman may be found in the url parameters in thecongressman profile from the site: http://www2.camara.leg.br/', max_length=30, null=True, verbose_name='Congressman ID', blank=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='avatar',
            field=image_cropping.fields.ImageCropField(blank=True, upload_to='avatars/', null=True, verbose_name='profile picture', validators=[wikilegis.auth2.models.avatar_validation]),
        ),
        migrations.AlterField(
            model_name='user',
            name=b'cropping',
            field=image_cropping.fields.ImageRatioField('avatar', '70x70', hide_image_field=False, size_warning=False, allow_fullsize=False, free_crop=False, adapt_rotation=False, help_text='Note that the preview above will only be updated after you submit the form.', verbose_name='cropping'),
        ),
    ]
