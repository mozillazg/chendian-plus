# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sn', models.IntegerField(verbose_name='\u7f16\u53f7', db_index=True)),
                ('qq', models.CharField(max_length=50, verbose_name='QQ')),
                ('nick_name', models.CharField(max_length=50, verbose_name='\u6635\u79f0')),
                ('description', models.TextField(default='', verbose_name='\u7b80\u4ecb', blank=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('user', models.OneToOneField(verbose_name='user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'member',
                'verbose_name_plural': 'members',
            },
            bases=(models.Model,),
        ),
    ]
