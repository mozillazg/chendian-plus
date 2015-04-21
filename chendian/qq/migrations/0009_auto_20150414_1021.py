# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('qq', '0008_uploadrecord_text'),
    ]

    operations = [
        migrations.AlterField(
            model_name='checkinrecord',
            name='book_name',
            field=models.TextField(default='', verbose_name='\u4e66\u540d', blank=True),
        ),
        migrations.AlterField(
            model_name='checkinrecord',
            name='nick_name',
            field=models.TextField(verbose_name='\u6635\u79f0'),
        ),
        migrations.AlterField(
            model_name='checkinrecord',
            name='qq',
            field=models.TextField(verbose_name='QQ'),
        ),
        migrations.AlterField(
            model_name='rawmessage',
            name='nick_name',
            field=models.TextField(verbose_name='\u6635\u79f0'),
        ),
        migrations.AlterField(
            model_name='rawmessage',
            name='qq',
            field=models.TextField(verbose_name='QQ'),
        ),
    ]
