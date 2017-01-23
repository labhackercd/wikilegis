# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-19 18:57
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0008_alter_user_username_max_length'),
        ('contenttypes', '0002_remove_content_type_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Bill',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='modified')),
                ('title', models.CharField(max_length=255, verbose_name='subject')),
                ('epigraph', models.CharField(max_length=255, null=True, verbose_name='epigraph')),
                ('description', models.TextField(verbose_name='description')),
                ('closing_date', models.DateField(verbose_name='closing date')),
                ('allowed_users', models.ManyToManyField(blank=True, related_name='allowed_bills', to=settings.AUTH_USER_MODEL, verbose_name='allowed users')),
                ('editors', models.ManyToManyField(blank=True, help_text='Any users in any of these groups will have permission to change this document.', to='auth.Group', verbose_name='editors')),
                ('reporting_member', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='reporting member')),
            ],
            options={
                'verbose_name': 'Bill',
                'verbose_name_plural': 'Bills',
            },
        ),
        migrations.CreateModel(
            name='BillSegment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='modified')),
                ('order', models.PositiveIntegerField(default=0, verbose_name='order')),
                ('number', models.CharField(blank=True, max_length=200, null=True, verbose_name='number')),
                ('original', models.BooleanField(default=True, verbose_name='original')),
                ('content', models.TextField(verbose_name='content')),
                ('author', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='author')),
                ('bill', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='segments', to='core.Bill', verbose_name='bill')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='core.BillSegment', verbose_name='segment parent')),
                ('replaced', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='substitutes', to='core.BillSegment', verbose_name='segment replaced')),
            ],
            options={
                'verbose_name': 'segment',
                'verbose_name_plural': 'segments',
                'ordering': ('order',),
            },
        ),
        migrations.CreateModel(
            name='BillStatus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=50, verbose_name='description')),
                ('slug', models.SlugField(verbose_name='slug')),
            ],
            options={
                'verbose_name': 'Bill Status',
                'verbose_name_plural': 'Bill Status',
            },
        ),
        migrations.CreateModel(
            name='BillTheme',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=50, verbose_name='description')),
                ('slug', models.SlugField(verbose_name='slug')),
            ],
            options={
                'verbose_name': 'Bill Theme',
                'verbose_name_plural': 'Bill Themes',
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='modified')),
                ('text', models.CharField(max_length=500, verbose_name='text')),
                ('object_id', models.PositiveIntegerField()),
                ('author', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='author')),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.ContentType')),
            ],
            options={
                'verbose_name': 'Segment Comment',
                'verbose_name_plural': 'Segment Comments',
            },
        ),
        migrations.CreateModel(
            name='SegmentType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='name')),
                ('apresentation_name', models.CharField(blank=True, max_length=200, null=True, verbose_name='apresentation name')),
                ('editable', models.BooleanField(default='True', verbose_name='editable')),
            ],
            options={
                'verbose_name': 'Segment Type',
                'verbose_name_plural': 'Segment Types',
            },
        ),
        migrations.CreateModel(
            name='UpDownVote',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='modified')),
                ('object_id', models.PositiveIntegerField()),
                ('vote', models.BooleanField(choices=[(True, 'Up Vote'), (False, 'Down Vote')], default=False)),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.ContentType')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='user')),
            ],
        ),
        migrations.AddField(
            model_name='billsegment',
            name='segment_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.SegmentType', verbose_name='type'),
        ),
        migrations.AddField(
            model_name='bill',
            name='status',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.BillStatus', verbose_name='status'),
        ),
        migrations.AddField(
            model_name='bill',
            name='theme',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.BillTheme', verbose_name='theme'),
        ),
        migrations.AlterUniqueTogether(
            name='updownvote',
            unique_together=set([('user', 'object_id', 'content_type')]),
        ),
        migrations.AlterUniqueTogether(
            name='comment',
            unique_together=set([('object_id', 'content_type')]),
        ),
    ]
