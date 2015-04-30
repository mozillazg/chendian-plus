# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('qq', '0009_auto_20150414_1021'),
    ]

    operations = [
        migrations.AlterField(
            model_name='checkinrecord',
            name='book_name',
            field=models.TextField(default='', db_index=True, verbose_name='\u4e66\u540d', blank=True),
        ),
    ]
