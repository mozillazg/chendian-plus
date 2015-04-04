# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('member', '0002_newmember'),
    ]

    operations = [
        migrations.AlterField(
            model_name='newmember',
            name='status',
            field=models.SmallIntegerField(default=0, choices=[(0, '\u5f85\u5904\u7406'), (1, '\u63a5\u53d7'), (2, '\u4e0d\u63a5\u53d7')]),
            preserve_default=True,
        ),
    ]
