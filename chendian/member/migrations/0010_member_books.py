# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0010_book_author'),
        ('member', '0009_auto_20150502_1640'),
    ]

    operations = [
        migrations.AddField(
            model_name='member',
            name='books',
            field=models.ManyToManyField(related_name='readers', to='book.Book'),
        ),
    ]
