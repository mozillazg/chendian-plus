# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('qq', '0002_auto_20150304_2322'),
    ]

    operations = [
        migrations.AddField(
            model_name='checkinrecord',
            name='raw_msg',
            field=models.OneToOneField(default=0, verbose_name='\u539f\u59cb\u804a\u5929\u8bb0\u5f55', to='qq.RawMessage'),
            preserve_default=False,
        ),
    ]
