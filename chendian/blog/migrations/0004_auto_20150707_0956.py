# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_auto_20150704_1159'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='article',
            options={'ordering': ['-created_at']},
        ),
        migrations.AlterModelOptions(
            name='category',
            options={'ordering': ['-created_at']},
        ),
        migrations.AlterModelOptions(
            name='tag',
            options={'ordering': ['-created_at']},
        ),
        migrations.AlterField(
            model_name='article',
            name='author',
            field=models.ForeignKey(blank=True, to='member.Member', null=True),
        ),
        migrations.AlterField(
            model_name='article',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now, db_index=True),
        ),
    ]
