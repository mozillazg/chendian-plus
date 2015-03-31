# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('qq', '0006_auto_20150311_2218'),
    ]

    operations = [
        migrations.AddField(
            model_name='checkinrecord',
            name='deleted',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
