# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('member', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='NewMember',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sn', models.IntegerField(verbose_name='\u7f16\u53f7')),
                ('qq', models.CharField(max_length=50, verbose_name='QQ')),
                ('nick_name', models.CharField(max_length=50, verbose_name='\u6635\u79f0')),
                ('description', models.TextField(default='', verbose_name='\u7b80\u4ecb', blank=True)),
                ('status', models.CharField(default='', max_length=10, choices=[('', '\u5f85\u5904\u7406'), ('approve', '\u63a5\u53d7'), ('disapprove', '\u4e0d\u63a5\u53d7')])),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(default=django.utils.timezone.now)),
            ],
            options={
                'verbose_name': 'new_member',
                'verbose_name_plural': 'new_members',
            },
            bases=(models.Model,),
        ),
    ]
