#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from django.db import models
from django.utils.timezone import now
from django.utils.encoding import python_2_unicode_compatible

from core.db import LogicalDeleteMixin, ValidObjectManager
from core.utils import utc_to_local


class ReversePostedAtManager(ValidObjectManager):
    def get_queryset(self):
        return super(ReversePostedAtManager, self
                     ).get_queryset().order_by('-posted_at')


@python_2_unicode_compatible
class RawMessage(LogicalDeleteMixin):
    nick_name = models.TextField('昵称')
    qq = models.TextField('QQ')
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
class CheckinRecord(LogicalDeleteMixin):
    raw_msg = models.OneToOneField(RawMessage, verbose_name='原始聊天记录')

    nick_name = models.TextField('昵称')
    sn = models.IntegerField('编号', blank=True, null=True, db_index=True)
    qq = models.TextField('QQ', db_index=True)
    book_name = models.TextField('书名', blank=True, default='', db_index=True)
    think = models.TextField('读后感', default='', blank=True)
    posted_at = models.DateTimeField('打卡时间', db_index=True)

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
class UploadRecord(LogicalDeleteMixin):
    status_progress = 1
    status_finish = 2
    status_error = 3
    status_choices = (
        (status_progress, '处理中'),
        (status_finish, '完成'),
        (status_error, '错误'),
    )
    status = models.SmallIntegerField(choices=status_choices,
                                      default=status_progress)
    type_qq = 1
    type_lofter = 2
    type_hundred_goal_note = 3
    type_choices = (
        (type_qq, 'QQ 群聊天记录(txt)'),
        (type_lofter, 'Lofter 博客导出的文件(xml)'),
        (type_hundred_goal_note, '百日斩打卡记录(html)'),
    )
    type = models.SmallIntegerField(choices=type_choices,
                                    default=type_qq)
    count = models.IntegerField(default=0)
    error = models.TextField(default='')
    text = models.TextField(default='')

    created_at = models.DateTimeField(default=now)
    update_at = models.DateTimeField(default=now)

    class Meta:
        verbose_name = '上传记录'
        verbose_name_plural = '上传记录'

    def __str__(self):
        return '{0} at {1}'.format(self.update_at, self.status)

    def re_do(self):
        """重新分析记录"""
        from blog.utils import import_lofter
        from qq.utils import save_uploaded_text
        if self.type == self.type_qq:
            save_uploaded_text.delay(self.pk)
        else:
            import_lofter.delay(self.pk)
