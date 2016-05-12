#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.utils.timezone import now
from django.utils.encoding import python_2_unicode_compatible

from core.db import LogicalDeleteMixin
from core.utils import utc_to_local
from book.models import Book
from qq.models import CheckinRecord


@python_2_unicode_compatible
class Member(LogicalDeleteMixin):
    DEFAULT_AVATAR = settings.DEFAULT_MEMBER_AVATAR

    user = models.OneToOneField(User, related_name='member')

    sn = models.IntegerField('编号', db_index=True)
    qq = models.TextField('QQ', blank=True)
    nick_name = models.TextField('昵称', db_index=True, blank=True)
    avatar = models.URLField('头像', blank=True, default=DEFAULT_AVATAR)
    description = models.TextField('个人介绍', blank=True, default='个人介绍')
    books = models.ManyToManyField(Book, related_name='readers', blank=True)

    created_at = models.DateTimeField(default=now)
    updated_at = models.DateTimeField(default=now)
    last_read_at = models.DateTimeField(
        '最后一次读书时间', null=True, blank=True
    )

    class Meta:
        verbose_name = 'member'
        verbose_name_plural = 'members'

    def __str__(self):
        return '[{0}]{1}-{2}'.format(self.pk, self.sn, self.nick_name)

    def save(self, *args, **kwargs):
        from qq.utils import update_member_info, update_member_books
        if not self.avatar:
            self.avatar = self.DEFAULT_AVATAR

        self.updated_at = now()
        if not (self.pk and self.user):
            user = User.objects.filter(username=self.qq)
            if not user.exists():
                user = User.objects.create_user(self.qq)
                user.set_password(settings.DEFAULT_PASSWORD)
                user.save()
            else:
                user = user[0]
            self.user = user

        new = (not self.pk)
        value = super(Member, self).save(*args, **kwargs)
        self.update_qq_record()
        if new:
            update_member_info.delay(self.pk)
            update_member_books.delay(self.pk)

        return value

    def update_qq_record(self):
        CheckinRecord.raw_objects.filter(qq=self.qq).update(
            sn=self.sn, nick_name=self.nick_name
        )


@python_2_unicode_compatible
class NewMember(LogicalDeleteMixin):
    status_need = 0
    status_approve = 1
    status_disappreove = 2
    status_choices = (
        (status_need, '待处理'),
        (status_approve, '接受'),
        (status_disappreove, '不接受'),
    )

    sn = models.IntegerField('编号')
    qq = models.TextField('QQ')
    nick_name = models.TextField('昵称')
    description = models.TextField('个人介绍', blank=True, default='个人介绍')
    status = models.SmallIntegerField(choices=status_choices,
                                      default=status_need)

    created_at = models.DateTimeField(default=now)
    updated_at = models.DateTimeField(default=now)
    last_read_at = models.DateTimeField(
        '最后一次读书时间', null=True, blank=True
    )

    class Meta:
        verbose_name = 'new_member'
        verbose_name_plural = 'new_members'

    def __str__(self):
        return 'New Member: 【{0}】{1}'.format(self.sn, self.nick_name)

    def approve(self):
        from qq.utils import update_member_info, update_member_books
        m = Member.raw_objects.filter(qq=self.qq).first()
        if m is None:
            m = Member()
        m.sn = self.sn
        m.qq = self.qq
        m.nick_name = self.nick_name
        m.description = self.description
        m.last_read_at = self.last_read_at
        m.save()
        update_member_info.delay(m.pk)
        update_member_books.delay(m.pk)

        self.status = self.status_approve
        self.save()
        return m

    def disapprove(self):
        self.status = self.status_disappreove
        self.save()


@python_2_unicode_compatible
class CheckinCount(LogicalDeleteMixin):
    member = models.ForeignKey(Member)
    count = models.IntegerField(default=0, verbose_name='连续打卡天数')
    checkined_at = models.DateTimeField(verbose_name='打卡日期')
    checkins = models.ManyToManyField('qq.CheckinRecord')

    class Meta:
        verbose_name_plural = verbose_name = '连续打卡记录'

    def __str__(self):
        return '{}'.format(self.member)

    @property
    def checkined_at_local(self):
        return utc_to_local(self.checkined_at)
