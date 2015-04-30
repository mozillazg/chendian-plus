# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0003_auto_20150414_1021'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='isbn',
            field=models.TextField(default='', blank=True),
        ),
    ]
