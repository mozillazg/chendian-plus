# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('qq', '0005_auto_20150308_1347'),
    ]

    operations = [
        migrations.AlterField(
            model_name='checkinrecord',
            name='posted_at',
            field=models.DateTimeField(verbose_name='\u6253\u5361\u65f6\u95f4', db_index=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='checkinrecord',
            name='sn',
            field=models.IntegerField(db_index=True, null=True, verbose_name='\u7f16\u53f7', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='rawmessage',
            name='posted_at',
            field=models.DateTimeField(verbose_name='\u53d1\u8a00\u65f6\u95f4', db_index=True),
            preserve_default=True,
        ),
    ]
