# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0007_auto_20150429_1406'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='deleted',
            field=models.BooleanField(default=False),
        ),
    ]
