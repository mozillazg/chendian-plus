# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('member', '0004_auto_20150414_1021'),
    ]

    operations = [
        migrations.AddField(
            model_name='newmember',
            name='last_read_at',
            field=models.DateTimeField(null=True, verbose_name='\u6700\u540e\u4e00\u6b21\u8bfb\u4e66\u65f6\u95f4', blank=True),
        ),
    ]
