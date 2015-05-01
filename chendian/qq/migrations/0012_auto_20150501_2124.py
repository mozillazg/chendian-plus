# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('qq', '0011_auto_20150429_1437'),
    ]

    operations = [
        migrations.AddField(
            model_name='rawmessage',
            name='deleted',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='uploadrecord',
            name='deleted',
            field=models.BooleanField(default=False),
        ),
    ]
