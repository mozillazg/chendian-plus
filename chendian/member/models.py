#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from django.contrib.auth.models import User
from django.db import models
from django.utils.timezone import now
from django.utils.encoding import python_2_unicode_compatible

from qq.models import CheckinRecord


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

        value = super(Member, self).save(*args, **kwargs)
        self.update_qq_record()
        return value

    def update_qq_record(self):
        CheckinRecord.objects.filter(qq=self.qq).update(
            sn=self.sn, nick_name=self.nick_name
        )


@python_2_unicode_compatible
class NewMember(models.Model):
    status_need = 0
    status_approve = 1
    status_disappreove = 2
    status_choices = (
        (0, '待处理'),
        (1, '接受'),
        (2, '不接受'),
    )

    sn = models.IntegerField('编号')
    qq = models.CharField('QQ', max_length=50)
    nick_name = models.CharField('昵称', max_length=50)
    description = models.TextField('简介', blank=True, default='')
    status = models.SmallIntegerField(choices=status_choices,
                                      default=status_need)

    created_at = models.DateTimeField(default=now)
    updated_at = models.DateTimeField(default=now)

    class Meta:
        verbose_name = 'new_member'
        verbose_name_plural = 'new_members'

    def __str__(self):
        return 'New Member: 【{0}】{1}'.format(self.sn, self.nick_name)

    def approve(self):
        m = Member()
        m.sn = self.sn
        m.qq = self.qq
        m.nick_name = self.nick_name
        m.description = self.description
        m.save()

        self.status = self.status_approve
        self.save()
        return m

    def disapprove(self):
        self.status = self.status_disappreove
        self.save()
