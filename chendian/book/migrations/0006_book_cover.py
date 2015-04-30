# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0005_auto_20150428_2125'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='cover',
            field=models.URLField(default='', verbose_name='\u5c01\u9762', blank=True),
        ),
    ]
