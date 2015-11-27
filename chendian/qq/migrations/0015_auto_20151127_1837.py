# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('qq', '0014_uploadrecord_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='uploadrecord',
            name='type',
            field=models.SmallIntegerField(default=1, choices=[(1, 'QQ \u7fa4\u804a\u5929\u8bb0\u5f55(txt)'), (2, 'Lofter \u535a\u5ba2\u5bfc\u51fa\u7684\u6587\u4ef6(xml)'), (3, '\u767e\u65e5\u65a9\u6253\u5361\u8bb0\u5f55(html)')]),
        ),
    ]
