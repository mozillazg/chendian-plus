# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_auto_20150707_1118'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='markup',
            field=models.SmallIntegerField(default=0, choices=[(2, 'HTML'), (0, 'Markdown'), (1, 'reStructuredText')]),
        ),
    ]
