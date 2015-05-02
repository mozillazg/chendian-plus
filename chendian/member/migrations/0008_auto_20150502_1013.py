# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('member', '0007_auto_20150501_2124'),
    ]

    operations = [
        migrations.AddField(
            model_name='member',
            name='avatar',
            field=models.URLField(default='http://tmp-images.qiniudn.com/chendian/cat_mouse_reading.jpg', verbose_name='\u5934\u50cf', blank=True),
        ),
        migrations.AlterField(
            model_name='member',
            name='description',
            field=models.TextField(default='', verbose_name='\u4e2a\u4eba\u4ecb\u7ecd', blank=True),
        ),
    ]
