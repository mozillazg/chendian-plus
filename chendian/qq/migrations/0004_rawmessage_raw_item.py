# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('qq', '0003_checkinrecord_raw_msg'),
    ]

    operations = [
        migrations.AddField(
            model_name='rawmessage',
            name='raw_item',
            field=models.TextField(default='', verbose_name='\u6574\u4e2a\u8bb0\u5f55\u5185\u5bb9'),
            preserve_default=True,
        ),
    ]
