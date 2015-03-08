# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('qq', '0004_rawmessage_raw_item'),
    ]

    operations = [
        migrations.CreateModel(
            name='UploadRecord',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('status', models.SmallIntegerField(default=1, choices=[(1, '\u5904\u7406\u4e2d'), (2, '\u5b8c\u6210'), (3, '\u9519\u8bef')])),
                ('count', models.IntegerField(default=0)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('update_at', models.DateTimeField(default=django.utils.timezone.now)),
            ],
            options={
                'verbose_name': '\u4e0a\u4f20\u8bb0\u5f55',
                'verbose_name_plural': '\u4e0a\u4f20\u8bb0\u5f55',
            },
            bases=(models.Model,),
        ),
        migrations.AlterField(
            model_name='checkinrecord',
            name='book_name',
            field=models.CharField(max_length=100, verbose_name='\u4e66\u540d', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='checkinrecord',
            name='think',
            field=models.TextField(default='', verbose_name='\u8bfb\u540e\u611f', blank=True),
            preserve_default=True,
        ),
    ]
