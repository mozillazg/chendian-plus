# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0008_book_deleted'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='raw_name',
            field=models.TextField(default=''),
        ),
    ]
