#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from django.contrib.auth.models import User
from django.db import models
from django.utils.timezone import now
from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible
class Member(models.Model):
    user = models.OneToOneField(User, verbose_name='user')

    sn = models.IntegerField('编号', db_index=True)
    qq = models.CharField('QQ', max_length=50)
    nick_name = models.CharField('昵称', max_length=50)
    description = models.TextField('简介', blank=True, default='')

    created_at = models.DateTimeField(default=now)
    updated_at = models.DateTimeField(default=now)

    class Meta:
        verbose_name = 'member'
        verbose_name_plural = 'members'

    def __str__(self):
        return '【{0}】{1}'.format(self.sn, self.nick_name)

    def save(self, *args, **kwargs):
        self.updated_at = now()
        if not (self.pk and self.user):
            user = User.objects.filter(username=self.qq)
            if not user.exists():
                user = User.objects.create_user(self.qq)
                user.save()
            else:
                user = user[0]
            self.user = user

        return super(Member, self).save(*args, **kwargs)
