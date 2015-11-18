# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
import core.db


class Migration(migrations.Migration):

    dependencies = [
        ('member', '0012_auto_20150806_2144'),
        ('book', '0011_auto_20150516_0918'),
    ]

    operations = [
        migrations.CreateModel(
            name='HundredGoalNote',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('deleted', models.BooleanField(default=False)),
                ('book_name', models.CharField(max_length=100)),
                ('author_name', models.CharField(max_length=80)),
                ('note', models.TextField(default='', blank='')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('book', models.ForeignKey(blank=True, to='book.Book', null=True)),
                ('member', models.ForeignKey(blank=True, to='member.Member', null=True)),
            ],
            options={
                'verbose_name': '\u767e\u65e5\u65a9\u6253\u5361\u8bb0\u5f55',
                'verbose_name_plural': '\u767e\u65e5\u65a9\u6253\u5361\u8bb0\u5f55',
            },
            bases=(core.db.CachingMixin, models.Model),
        ),
    ]
