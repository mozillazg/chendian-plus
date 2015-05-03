# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0009_book_raw_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='author',
            field=models.TextField(default=''),
        ),
    ]
