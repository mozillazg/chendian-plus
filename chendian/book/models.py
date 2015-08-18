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
        if self.pk:
            old = Book.raw_objects.get(pk=self.pk)
            if self.name != old.name:
                CheckinRecord.raw_objects.filter(book_name=old.name).update(
                    book_name=self.name
                )

        return super(Book, self).save(*args, **kwargs)
