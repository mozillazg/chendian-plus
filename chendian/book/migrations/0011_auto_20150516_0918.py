# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0010_book_author'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='cover',
            field=models.URLField(default='http://tmp-images.qiniudn.com/chendian/cover_template.jpg', verbose_name='\u5c01\u9762', blank=True),
        ),
    ]
