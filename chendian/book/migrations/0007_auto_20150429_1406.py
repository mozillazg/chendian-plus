# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0006_book_cover'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='last_read_at',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='book',
            name='read_count',
            field=models.IntegerField(default=0, verbose_name='\u9605\u8bfb\u672c\u4e66\u7684\u4eba\u6570'),
        ),
    ]
