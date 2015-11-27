# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0013_book_tags'),
    ]

    operations = [
        migrations.AddField(
            model_name='hundredgoalnote',
            name='author_url',
            field=models.CharField(default='', max_length=100),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='book',
            name='last_read_at',
            field=models.DateTimeField(db_index=True, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='hundredgoalnote',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now, db_index=True),
        ),
    ]
