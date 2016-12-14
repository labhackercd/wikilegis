# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0020_bill_allowed_users'),
    ]

    operations = [
        migrations.CreateModel(
            name='BillReference',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='modified')),
                ('name', models.CharField(max_length=200, null=True, verbose_name='Nome', blank=True)),
                ('file', models.FileField(upload_to='bill/files/')),
            ],
            options={
                'verbose_name': 'reference',
                'verbose_name_plural': 'references',
            },
        ),
        migrations.AlterField(
            model_name='bill',
            name='allowed_users',
            field=models.ManyToManyField(related_name='allowed_bills', verbose_name='allowed users', to=settings.AUTH_USER_MODEL, blank=True),
        ),
        migrations.AlterField(
            model_name='bill',
            name='status',
            field=models.CharField(default='1', max_length=20, verbose_name='status', choices=[('draft', 'Draft'), ('unlisted', 'Unlisted'), ('published', 'Published'), ('closed', 'Closed')]),
        ),
        migrations.AddField(
            model_name='billreference',
            name='bill',
            field=models.ForeignKey(related_name='references', verbose_name='bill', to='core.Bill'),
        ),
    ]
