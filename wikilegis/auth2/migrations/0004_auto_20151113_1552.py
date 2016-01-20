# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import image_cropping.fields
import wikilegis.auth2.models


class Migration(migrations.Migration):

    dependencies = [
        ('auth2', '0003_auto_20151110_1304'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='id_congressman',
            field=models.CharField(help_text='The id of each congressman may be found in the url parameters in thecongressman profile from the site: http://www2.camara.leg.br/', max_length=30, null=True, verbose_name='Congressman ID', blank=True),
        ),
    ]
