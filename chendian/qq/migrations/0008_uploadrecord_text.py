# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('qq', '0007_checkinrecord_deleted'),
    ]

    operations = [
        migrations.AddField(
            model_name='uploadrecord',
            name='text',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
    ]
