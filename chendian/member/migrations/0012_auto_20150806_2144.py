# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('member', '0011_auto_20150707_1118'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='books',
            field=models.ManyToManyField(related_name='readers', to='book.Book', blank=True),
        ),
        migrations.AlterField(
            model_name='member',
            name='nick_name',
            field=models.TextField(db_index=True, verbose_name='\u6635\u79f0', blank=True),
        ),
        migrations.AlterField(
            model_name='member',
            name='qq',
            field=models.TextField(verbose_name='QQ', blank=True),
        ),
    ]
