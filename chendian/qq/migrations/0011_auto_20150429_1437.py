# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('qq', '0010_auto_20150428_2125'),
    ]

    operations = [
        migrations.AlterField(
            model_name='checkinrecord',
            name='qq',
            field=models.TextField(verbose_name='QQ', db_index=True),
        ),
    ]
