# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('member', '0010_member_books'),
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=100)),
                ('slug', models.CharField(max_length=255, blank=True)),
                ('summary', models.CharField(default='', max_length=500, blank=True)),
                ('content', models.TextField()),
                ('markup', models.SmallIntegerField(default=0, choices=[(0, 'Markdown'), (1, 'reStructuredText'), (2, 'HTML')])),
                ('image', models.URLField(default='', blank=True)),
                ('status', models.SmallIntegerField(default=0, choices=[(0, '\u8349\u7a3f'), (1, '\u5f85\u5ba1\u6838'), (2, '\u5ba1\u6838\u901a\u8fc7'), (3, '\u5ba1\u6838\u672a\u901a\u8fc7')])),
                ('sticky', models.BooleanField(default=False, verbose_name='\u662f\u5426\u7f6e\u9876')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('author', models.ForeignKey(to='member.Member', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('slug', models.CharField(max_length=150, blank=True)),
                ('description', models.CharField(default='', max_length=100, blank=True)),
                ('detail', models.TextField(default='', blank=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('slug', models.CharField(max_length=150, blank=True)),
                ('description', models.CharField(default='', max_length=100, blank=True)),
                ('detail', models.TextField(default='', blank=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.AddField(
            model_name='article',
            name='categories',
            field=models.ManyToManyField(to='blog.Category', blank=True),
        ),
        migrations.AddField(
            model_name='article',
            name='tags',
            field=models.ManyToManyField(to='blog.Tag', blank=True),
        ),
    ]
