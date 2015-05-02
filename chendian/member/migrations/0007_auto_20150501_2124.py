# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('member', '0006_member_last_read_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='member',
            name='deleted',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='newmember',
            name='deleted',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='member',
            name='user',
            field=models.OneToOneField(related_name='member', to=settings.AUTH_USER_MODEL),
        ),
    ]
