#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible


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
    posted_at = models.DateTimeField('发言时间')

    objects = models.Manager()
    sorted_objects = ReversePostedAtManager()

    class Meta:
        verbose_name = '聊天记录'
        verbose_name_plural = '聊天记录'

    def __str__(self):
        return '{0} at {1}'.format(self.nick_name, self.posted_at)


@python_2_unicode_compatible
class CheckinRecord(models.Model):
    raw_msg = models.OneToOneField(RawMessage, verbose_name='原始聊天记录')

    nick_name = models.CharField('昵称', max_length=50)
    models.CharField('昵称', max_length=50)
    sn = models.IntegerField('编号', blank=True, null=True)
    qq = models.CharField('QQ', max_length=50)
    book_name = models.CharField('书名', max_length=100)
    think = models.TextField('读后感', default='')
    posted_at = models.DateTimeField('打卡时间')

    objects = models.Manager()
    sorted_objects = ReversePostedAtManager()

    class Meta:
        verbose_name = '打卡记录'
        verbose_name_plural = '打卡记录'

    def __str__(self):
        return '{0} at {1}'.format(self.nick_name, self.posted_at)
