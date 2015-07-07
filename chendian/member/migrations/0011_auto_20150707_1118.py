# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('member', '0010_member_books'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='nick_name',
            field=models.TextField(verbose_name='\u6635\u79f0', db_index=True),
        ),
    ]
