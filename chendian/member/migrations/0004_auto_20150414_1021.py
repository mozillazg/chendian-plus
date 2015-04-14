# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('member', '0003_auto_20150331_1627'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='nick_name',
            field=models.TextField(verbose_name='\u6635\u79f0'),
        ),
        migrations.AlterField(
            model_name='member',
            name='qq',
            field=models.TextField(verbose_name='QQ'),
        ),
        migrations.AlterField(
            model_name='newmember',
            name='nick_name',
            field=models.TextField(verbose_name='\u6635\u79f0'),
        ),
        migrations.AlterField(
            model_name='newmember',
            name='qq',
            field=models.TextField(verbose_name='QQ'),
        ),
    ]
