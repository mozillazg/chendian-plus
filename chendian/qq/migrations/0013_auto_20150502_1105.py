# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('qq', '0012_auto_20150501_2124'),
    ]

    operations = [
        migrations.AddField(
            model_name='uploadrecord',
            name='error',
            field=models.TextField(default=''),
        ),
        migrations.AlterField(
            model_name='uploadrecord',
            name='text',
            field=models.TextField(default=''),
        ),
    ]
