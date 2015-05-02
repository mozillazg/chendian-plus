# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('member', '0008_auto_20150502_1013'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='description',
            field=models.TextField(default='\u4e2a\u4eba\u4ecb\u7ecd', verbose_name='\u4e2a\u4eba\u4ecb\u7ecd', blank=True),
        ),
        migrations.AlterField(
            model_name='newmember',
            name='description',
            field=models.TextField(default='\u4e2a\u4eba\u4ecb\u7ecd', verbose_name='\u4e2a\u4eba\u4ecb\u7ecd', blank=True),
        ),
    ]
