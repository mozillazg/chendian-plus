#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from django.db import models
from django.utils.timezone import now
from django.utils.encoding import python_2_unicode_compatible

from core.utils import utc_to_local


class ReversePostedAtManager(models.Manager):
    def get_queryset(self):
        return super(ReversePostedAtManager, self).get_queryset().order_by(
            '-posted_at'
        )


@python_2_unicode_compatible
class RawMessage(models.Model):
    nick_name = models.CharField('昵称', max_length=50)
    qq = models.CharField('QQ', max_length=50)
    sn = models.IntegerField('编号', blank=True, null=True)
    msg = models.TextField('消息内容', default='')
    raw_item = models.TextField('整个记录内容', default='')
    posted_at = models.DateTimeField('发言时间', db_index=True)

    objects = models.Manager()
    sorted_objects = ReversePostedAtManager()

    class Meta:
        verbose_name = '聊天记录'
        verbose_name_plural = '聊天记录'

    @property
    def posted_at_local(self):
        return utc_to_local(self.posted_at)

    def __str__(self):
        return '{0} at {1}'.format(self.nick_name, self.posted_at)


@python_2_unicode_compatible
class CheckinRecord(models.Model):
    raw_msg = models.OneToOneField(RawMessage, verbose_name='原始聊天记录')

    nick_name = models.CharField('昵称', max_length=50)
    sn = models.IntegerField('编号', blank=True, null=True, db_index=True)
    qq = models.CharField('QQ', max_length=50)
    book_name = models.CharField('书名', max_length=100, blank=True)
    think = models.TextField('读后感', default='', blank=True)
    posted_at = models.DateTimeField('打卡时间', db_index=True)

    objects = models.Manager()
    sorted_objects = ReversePostedAtManager()

    class Meta:
        verbose_name = '打卡记录'
        verbose_name_plural = '打卡记录'

    @property
    def posted_at_local(self):
        return utc_to_local(self.posted_at)

    def __str__(self):
        return '{0} at {1}'.format(self.nick_name, self.posted_at)


@python_2_unicode_compatible
class UploadRecord(models.Model):
    status_progress = 1
    status_finish = 2
    status_error = 3
    status_choices = (
        (1, '处理中'),
        (2, '完成'),
        (3, '错误'),
    )

    status = models.SmallIntegerField(choices=status_choices, default=1)
    count = models.IntegerField(default=0)

    created_at = models.DateTimeField(default=now)
    update_at = models.DateTimeField(default=now)

    class Meta:
        verbose_name = '上传记录'
        verbose_name_plural = '上传记录'

    def __str__(self):
        return '{0} at {1}'.format(self.update_at, self.status)
