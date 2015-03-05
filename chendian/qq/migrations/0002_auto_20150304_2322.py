# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('qq', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='checkinrecord',
            name='nick_name',
            field=models.CharField(max_length=50, verbose_name='\u6635\u79f0'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='checkinrecord',
            name='qq',
            field=models.CharField(default='', max_length=50, verbose_name='QQ'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='rawmessage',
            name='nick_name',
            field=models.CharField(max_length=50, verbose_name='\u6635\u79f0'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='rawmessage',
            name='qq',
            field=models.CharField(default='', max_length=50, verbose_name='QQ'),
            preserve_default=False,
        ),
    ]
