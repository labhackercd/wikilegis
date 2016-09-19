# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0017_auto_20160808_1552'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bill',
            name='theme',
            field=models.CharField(default='documento', max_length=255, verbose_name='theme', choices=[('documento', 'Others'), ('adm-publica', 'Public Administration'), ('agropecuaria', 'Farming'), ('assistencia-social', 'Social Assistance'), ('cidades', 'Cities'), ('ciencia', 'Science'), ('comunicacao', 'Communication'), ('consumidor', 'Consumer'), ('cultura', 'Culture'), ('direito-e-justica', 'Law and Justice'), ('direitos-humanos', 'Human Rights'), ('economia', 'Economy'), ('educacao', 'Education'), ('esportes', 'Sports'), ('familia', 'Family'), ('industria', 'Industry'), ('institucional', 'Institutional'), ('meio-ambiente', 'Environment'), ('participacao-e-transparencia', 'Participation and Transparency'), ('politica', 'Policy'), ('previdencia', 'Foresight'), ('relacoes-exteriores', 'Foreign Affairs'), ('saude', 'Health'), ('seguranca', 'Security'), ('trabalho', 'Work'), ('transporte-e-transito', 'Transportation and Transit'), ('turismo', 'Tourism')]),
        ),
    ]
