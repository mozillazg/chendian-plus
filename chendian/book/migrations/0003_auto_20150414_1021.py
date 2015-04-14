# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0002_auto_20150331_1659'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='name',
            field=models.TextField(verbose_name='\u540d\u79f0'),
        ),
    ]
