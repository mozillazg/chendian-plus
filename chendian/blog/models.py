#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals
from functools import partial
import re

# from django.contrib.auth.models import User
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.timezone import now
from pypinyin import slug

from core.db import LogicalDeleteMixin
from member.models import Member

pinyin_slug = partial(slug, errors=lambda x: re.sub('[^-\w]+', '', x))
# pinyin_slug = partial(slug, errors='replace')


@python_2_unicode_compatible
class Category(LogicalDeleteMixin):
    name = models.CharField(max_length=50)
    slug = models.CharField(max_length=150, blank=True)
    description = models.CharField(max_length=100, default='', blank=True)
    detail = models.TextField(default='', blank=True)
    created_at = models.DateTimeField(default=now)
    updated_at = models.DateTimeField(default=now)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.updated_at = now()
        if not self.slug:
            self.slug = pinyin_slug(self.name)
        return super(Category, self).save(*args, **kwargs)


@python_2_unicode_compatible
class Tag(LogicalDeleteMixin):
    name = models.CharField(max_length=50)
    slug = models.CharField(max_length=150, blank=True)
    description = models.CharField(max_length=100, default='', blank=True)
    detail = models.TextField(default='', blank=True)
    created_at = models.DateTimeField(default=now)
    updated_at = models.DateTimeField(default=now)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.updated_at = now()
        if not self.slug:
            self.slug = pinyin_slug(self.name)
        return super(Tag, self).save(*args, **kwargs)


@python_2_unicode_compatible
class Article(LogicalDeleteMixin):
    author = models.ForeignKey(Member, null=True)
    title = models.CharField(max_length=255)
    slug = models.CharField(max_length=255, blank=True)
    categories = models.ManyToManyField(Category, blank=True)
    tags = models.ManyToManyField(Tag, blank=True)
    summary = models.CharField(max_length=500, default='', blank=True)
    content = models.TextField()

    MARKUP_MARKDOWN = 0
    MARKUP_RST = 1
    MARKUP_HTML = 2
    MARKUP_CHOICES = (
        (MARKUP_MARKDOWN, 'Markdown'),
        (MARKUP_RST, 'reStructuredText'),
        (MARKUP_HTML, 'HTML'),
    )
    markup = models.SmallIntegerField(
        choices=MARKUP_CHOICES, default=MARKUP_MARKDOWN
    )
    image = models.URLField(default='', blank=True)

    STATUS_DRAFT = 0
    STATUS_PRE_APPROVE = 1
    STATUS_APPROVED = 2
    STATUS_DISAPPROVED = 3
    STATUS_CHOICES = (
        (STATUS_DRAFT, '草稿'),
        (STATUS_PRE_APPROVE, '待审核'),
        (STATUS_APPROVED, '审核通过'),
        (STATUS_DISAPPROVED, '审核未通过'),
    )
    status = models.SmallIntegerField(
        choices=STATUS_CHOICES, default=STATUS_DRAFT
    )

    sticky = models.BooleanField('是否置顶', default=False)

    created_at = models.DateTimeField(default=now)
    updated_at = models.DateTimeField(default=now)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.pk is None and self.updated_at:
            pass
        else:
            self.updated_at = now()
        if not self.slug:
            self.slug = pinyin_slug(self.title)
        return super(Article, self).save(*args, **kwargs)
