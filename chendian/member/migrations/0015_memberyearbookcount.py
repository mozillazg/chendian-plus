# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import core.db


class Migration(migrations.Migration):

    dependencies = [
        ('member', '0014_memberyearbook'),
    ]

    operations = [
        migrations.CreateModel(
            name='MemberYearBookCount',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('deleted', models.BooleanField(default=False)),
                ('year', models.IntegerField(db_index=True)),
                ('count', models.IntegerField(default=0)),
                ('member', models.ForeignKey(to='member.Member')),
            ],
            options={
                'verbose_name': '\u67d0\u4eba\u67d0\u5e74\u8bfb\u8fc7\u591a\u5c11\u4e66',
                'verbose_name_plural': '\u67d0\u4eba\u67d0\u5e74\u8bfb\u8fc7\u591a\u5c11\u4e66',
            },
            bases=(core.db.CachingMixin, models.Model),
        ),
    ]
