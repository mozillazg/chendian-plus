# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('qq', '0013_auto_20150502_1105'),
    ]

    operations = [
        migrations.AddField(
            model_name='uploadrecord',
            name='type',
            field=models.SmallIntegerField(default=1, choices=[(1, 'QQ \u7fa4\u804a\u5929\u8bb0\u5f55'), (2, 'Lofter \u535a\u5ba2\u5bfc\u51fa\u7684\u6587\u4ef6')]),
        ),
    ]
