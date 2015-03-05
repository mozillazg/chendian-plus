# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CheckinRecord',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nick_name', models.CharField(max_length=100, verbose_name='\u6635\u79f0')),
                ('sn', models.IntegerField(null=True, verbose_name='\u7f16\u53f7', blank=True)),
                ('qq', models.IntegerField(null=True, verbose_name='QQ', blank=True)),
                ('book_name', models.CharField(max_length=100, verbose_name='\u4e66\u540d')),
                ('think', models.TextField(default='', verbose_name='\u8bfb\u540e\u611f')),
                ('posted_at', models.DateTimeField(verbose_name='\u6253\u5361\u65f6\u95f4')),
            ],
            options={
                'verbose_name': '\u6253\u5361\u8bb0\u5f55',
                'verbose_name_plural': '\u6253\u5361\u8bb0\u5f55',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='RawMessage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nick_name', models.CharField(max_length=100, verbose_name='\u6635\u79f0')),
                ('qq', models.IntegerField(null=True, verbose_name='QQ', blank=True)),
                ('sn', models.IntegerField(null=True, verbose_name='\u7f16\u53f7', blank=True)),
                ('msg', models.TextField(default='', verbose_name='\u6d88\u606f\u5185\u5bb9')),
                ('posted_at', models.DateTimeField(verbose_name='\u53d1\u8a00\u65f6\u95f4')),
            ],
            options={
                'verbose_name': '\u804a\u5929\u8bb0\u5f55',
                'verbose_name_plural': '\u804a\u5929\u8bb0\u5f55',
            },
            bases=(models.Model,),
        ),
    ]
