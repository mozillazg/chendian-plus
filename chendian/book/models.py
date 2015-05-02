#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from django.db import models
from django.utils.timezone import now
from django.utils.encoding import python_2_unicode_compatible

from core.db import LogicalDeleteMixin
from qq.models import CheckinRecord


@python_2_unicode_compatible
class Book(LogicalDeleteMixin):
    isbn = models.TextField(blank=True, default='')
    name = models.TextField('名称', db_index=True)
    cover = models.URLField('封面', blank=True, default='')
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
            old = Book.objects.get(pk=self.pk)
            if self.name != old.name:
                CheckinRecord.objects.filter(book_name=old.name).update(
                    book_name=self.name
                )

        return super(Book, self).save(*args, **kwargs)
