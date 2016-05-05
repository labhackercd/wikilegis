# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_bill_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='Proposition',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False,
                                        auto_created=True, primary_key=True)),
                ('type', models.CharField(max_length=200, null=True, verbose_name='type',
                                          blank=True)),
                ('number', models.CharField(max_length=50, null=True, verbose_name='number',
                                            blank=True)),
                ('year', models.CharField(max_length=4, null=True, verbose_name='year',
                                          blank=True)),
                ('name_proposition', models.CharField(max_length=200, null=True,
                                                      verbose_name='name proposition',
                                                      blank=True)),
                ('id_proposition', models.IntegerField(null=True, verbose_name='id proposition',
                                                       blank=True)),
                ('id_main_proposition', models.IntegerField(null=True, verbose_name=
                                                            'id main proposition', blank=True)),
                ('name_origin_proposition', models.CharField(max_length=200, null=True,
                                                             verbose_name=
                                                             'name origin proposition',
                                                             blank=True)),
                ('theme', models.CharField(max_length=200, null=True, verbose_name='theme',
                                           blank=True)),
                ('menu', models.TextField(null=True, verbose_name='menu', blank=True)),
                ('menu_explanation', models.TextField(null=True, verbose_name='menu_explanation',
                                                      blank=True)),
                ('author', models.CharField(max_length=200, null=True, verbose_name='author',
                                            blank=True)),
                ('id_register', models.CharField(max_length=200, null=True, verbose_name=
                                                 'id register', blank=True)),
                ('uf_author', models.CharField(max_length=200, null=True, verbose_name=
                                               'uf author', blank=True)),
                ('party_author', models.CharField(max_length=200, null=True, verbose_name=
                                                  'party author', blank=True)),
                ('apresentation_date', models.DateField(null=True, verbose_name=
                                                        'apresentation date', blank=True)),
                ('processing_regime', models.CharField(max_length=200, null=True, verbose_name=
                                                       'processing_regime', blank=True)),
                ('last_dispatch_date', models.DateField(null=True, verbose_name=
                                                        'last dispatch date', blank=True)),
                ('last_dispatch', models.TextField(null=True, verbose_name='last dispatch',
                                                   blank=True)),
                ('appraisal', models.CharField(max_length=200, null=True, verbose_name=
                                               'appraisal', blank=True)),
                ('indexing', models.CharField(max_length=200, null=True, verbose_name=
                                              'indexing', blank=True)),
                ('situation', models.CharField(max_length=200, null=True, verbose_name=
                                               'situation', blank=True)),
                ('content_link', models.URLField(null=True, verbose_name='content link',
                                                 blank=True)),
                ('bill', models.ForeignKey(verbose_name='bill', to='core.Bill')),
            ],
            options={
                'verbose_name': 'proposition',
                'verbose_name_plural': 'propositions',
            },
        ),
    ]
