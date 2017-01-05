# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import core.db


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0015_yearbook'),
        ('member', '0013_checkincount'),
    ]

    operations = [
        migrations.CreateModel(
            name='MemberYearBook',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('deleted', models.BooleanField(default=False)),
                ('year', models.IntegerField(db_index=True)),
                ('book', models.ForeignKey(to='book.Book')),
                ('member', models.ForeignKey(to='member.Member')),
            ],
            options={
                'verbose_name': '\u67d0\u4eba\u67d0\u5e74\u8bfb\u8fc7',
                'verbose_name_plural': '\u67d0\u4eba\u67d0\u5e74\u8bfb\u8fc7',
            },
            bases=(core.db.CachingMixin, models.Model),
        ),
    ]
