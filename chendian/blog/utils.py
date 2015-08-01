#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals
import datetime
import logging
import sys
import traceback

from django.utils.timezone import now
from django_rq import job
import pytz
import xmltodict

from member.models import Member
from qq.models import UploadRecord
from .models import Article, Tag

logger = logging.getLogger(__name__)


class Lofter(object):
    def __init__(self, created_at, updated_at, author_name, title, content,
                 summary='', markup=Article.MARKUP_HTML, tags=None,
                 type='text', photolinks='{}', embed='{}',
                 caption=''):
        self.created_at = created_at
        self.updated_at = updated_at
        self.author_name = author_name
        self.title = title
        self.content = content
        self.summary = summary
        self.markup = markup
        self.tags = tags or []
        self.type = type
        self.caption = caption
        self.photolinks = photolinks
        self.embed = embed

        if type == 'Photo':
            self.content = photolinks + '<br />' + caption
        elif type == 'Music':
            self.content = embed + '<br />' + caption

    def save_as_article(self):
        article = Article.objects.filter(created_at=self.created_at).first()
        if article is not None:
            return article

        article = Article.objects.create(
            created_at=self.created_at, updated_at=self.updated_at,
            markup=self.markup, summary=self.summary, content=self.content,
            title=self.title, author=self._get_author(),
            status=Article.STATUS_APPROVED
        )
        for tag in self._get_tags():
            article.tags.add(tag)

        return article

    def _get_author(self):
        if not self.author_name:
            return

        author = Member.objects.filter(nick_name=self.author_name).first()
        if author is not None:
            return author

    def _get_tags(self):
        if not self.tags:
            yield
            return

        for tag in self.tags:
            t = Tag.objects.filter(name=tag).first()
            if t is None:
                t = Tag.objects.create(name=tag)
            yield t

    def __getitem__(self, key):
        return self.__dict__[key]


class LofterParser(object):
    def __init__(self, xml):
        self.xml = xml

    def parse(self):
        for item in xmltodict.parse(self.xml)['lofterBlogExport']['PostItem']:
            yield self._parse(item)

    def _parse(self, item):
        created_at = self.convert_time(int(item['publishTime']))
        if item.get('modifyTime'):
            updated_at = self.convert_time(int(item['modifyTime']))
        else:
            updated_at = created_at
        author_name = item.get('content', '').split('</p>', 1)[0].replace('<p>', '')
        if '/' in author_name:
            author_name = author_name.split('/', 1)[1]
        title = item['title'] or ''
        content = item.get('content', '')
        tags = item.get('tag', '').split(',')
        type = item.get('type', '')

        caption = item.get('caption', '')
        photolinks = item.get('photoLinks', '{}')
        embed = item.get('embed', '{}')

        return Lofter(created_at, updated_at, author_name, title,
                      content, tags=tags, type=type,
                      photolinks=photolinks, embed=embed,
                      caption=caption)

    def convert_time(self, n):
        t = datetime.datetime.utcfromtimestamp(n / 1000.0)
        return t.replace(tzinfo=pytz.UTC)


@job
def import_lofter(pk):
    r = UploadRecord.raw_objects.get(pk=pk)
    xml = r.text
    try:
        n = 0
        for lofter in LofterParser(xml).parse():
            lofter.save_as_article()
            n = n + 1
        r.count = n
        r.status = UploadRecord.status_finish
    except Exception as e:
        logger.exception(e)
        exec_info = sys.exc_info()
        r.error = u'\n'.join(traceback.format_exception(*exec_info))
        r.status = UploadRecord.status_error
    r.update_at = now()
    r.error = ''
    r.save()
