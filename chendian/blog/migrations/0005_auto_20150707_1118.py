# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_auto_20150707_0956'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='slug',
            field=models.CharField(db_index=True, max_length=255, blank=True),
        ),
        migrations.AlterField(
            model_name='category',
            name='slug',
            field=models.CharField(db_index=True, max_length=150, blank=True),
        ),
        migrations.AlterField(
            model_name='tag',
            name='slug',
            field=models.CharField(db_index=True, max_length=150, blank=True),
        ),
    ]
