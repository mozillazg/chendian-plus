# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import core.db


class Migration(migrations.Migration):

    dependencies = [
        ('qq', '0015_auto_20151127_1837'),
        ('member', '0012_auto_20150806_2144'),
    ]

    operations = [
        migrations.CreateModel(
            name='CheckinCount',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('deleted', models.BooleanField(default=False)),
                ('count', models.IntegerField(default=0, verbose_name='\u8fde\u7eed\u6253\u5361\u5929\u6570')),
                ('checkined_at', models.DateTimeField(verbose_name='\u6253\u5361\u65e5\u671f')),
                ('checkins', models.ManyToManyField(to='qq.CheckinRecord')),
                ('member', models.ForeignKey(to='member.Member')),
            ],
            options={
                'verbose_name': '\u8fde\u7eed\u6253\u5361\u8bb0\u5f55',
                'verbose_name_plural': '\u8fde\u7eed\u6253\u5361\u8bb0\u5f55',
            },
            bases=(core.db.CachingMixin, models.Model),
        ),
    ]
