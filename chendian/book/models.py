#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from django.conf import settings
from django.db import models
from django.utils.timezone import now
from django.utils.encoding import python_2_unicode_compatible

from core.db import LogicalDeleteMixin
from qq.models import CheckinRecord


@python_2_unicode_compatible
class Book(LogicalDeleteMixin):
    DEFAULT_COVER = settings.DEFAULT_BOOK_COVER

    isbn = models.TextField(blank=True, default='')
    name = models.TextField('名称', db_index=True)
    raw_name = models.TextField(default='')
    author = models.TextField(default='')
    cover = models.URLField('封面', blank=True, default=DEFAULT_COVER)
    douban_url = models.URLField(blank=True, default='')
    description = models.TextField('简介', blank=True, default='')

    tags = models.ManyToManyField('blog.Tag', blank=True)
    created_at = models.DateTimeField(default=now)
    updated_at = models.DateTimeField(default=now)
    last_read_at = models.DateTimeField(null=True, blank=True)
    read_count = models.IntegerField('阅读本书的人数', default=0)

    class Meta:
        verbose_name = 'book'
        verbose_name_plural = 'books'

    def __str__(self):
        return '{0}'.format(self.name)

    def save(self, *args, **kwargs):
        self.updated_at = now()
        if self.pk:
            old = Book.raw_objects.get(pk=self.pk)
            if self.name != old.name:
                CheckinRecord.raw_objects.filter(book_name=old.name).update(
                    book_name=self.name
                )

        return super(Book, self).save(*args, **kwargs)


@python_2_unicode_compatible
class HundredGoalNote(LogicalDeleteMixin):
    """百人斩笔记"""
    book_name = models.CharField(max_length=100)
    book = models.ForeignKey(Book, null=True, blank=True)
    member = models.ForeignKey('member.Member', null=True, blank=True)
    author_name = models.CharField(max_length=80)
    note = models.TextField(default='', blank='')

    created_at = models.DateTimeField(default=now)
    updated_at = models.DateTimeField(default=now)

    class Meta:
        verbose_name = '百日斩打卡记录'
        verbose_name_plural = '百日斩打卡记录'

    def __str__(self):
        return '{0}'.format(self.book_name)

    def save(self, *args, **kwargs):
        self.updated_at = now()
        return super(HundredGoalNote, self).save(*args, **kwargs)
