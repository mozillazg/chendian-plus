# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import core.db


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0014_auto_20151127_1645'),
    ]

    operations = [
        migrations.CreateModel(
            name='YearBook',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('deleted', models.BooleanField(default=False)),
                ('year', models.IntegerField(db_index=True)),
                ('reader_count', models.IntegerField(default=0)),
                ('book', models.ForeignKey(to='book.Book')),
            ],
            options={
                'verbose_name': '\u67d0\u4e66\u67d0\u5e74',
                'verbose_name_plural': '\u67d0\u4e66\u67d0\u5e74',
            },
            bases=(core.db.CachingMixin, models.Model),
        ),
    ]
