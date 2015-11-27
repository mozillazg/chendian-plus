#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from collections import namedtuple
import datetime
from difflib import SequenceMatcher
import logging
import time

from django.conf import settings
from django.utils.timezone import now
import magic
import requests

from blog.models import Tag
from core.storage import Qiniu
from .models import Book
logger = logging.getLogger(__name__)


def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()


class UpdateBookInfoFromDouban(object):
    SEARCH_URL = 'https://api.douban.com/v2/book/search'
    SUBJECT_URL = 'http://book.douban.com/subject/{id}/'

    def __init__(self, verify=False):
        self.session = requests.Session()
        self.session.headers.update({
            'DNT': '1',
            'Accept-Encoding': 'gzip, deflate, sdch',
            'Accept-Language': 'en-US,en;q=0.8,zh-CN;q=0.6,zh;q=0.4',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2450.0 Iron/46.0.2450.0 Safari/537.36',  # noqa
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',  # noqa
            'Cache-Control': 'max-age=0',
        })
        self.verify = verify

    def search_book(self, book):
        url = self.SEARCH_URL
        params = {
            'q': book.name,
        }
        if settings.DOUBAN_APIKEY:
            params['apikey'] = settings.DOUBAN_APIKEY
        books = self.session.get(url, params=params, verify=self.verify
                                 ).json()['books']
        return books

    def best_match(self, name, books):
        match = namedtuple('Match', ['book', 'rate'])
        similar_rates = [
            match(book, similar(name, book['title']))
            for book in books
        ]
        min_rate = 0.5
        best_similar = similar_rates[0]
        for item in similar_rates:
            if item.rate > best_similar.rate:
                best_similar = item
        if best_similar.rate < min_rate:
            return
        else:
            return best_similar

    def update(self, book, data):
        if not book.author:
            book.author = ', '.join(data['author'])
        if not book.isbn:
            book.isbn = data.get('isbn13', '')
        if (not book.description) or book.description == book.name:
            book.description = data['summary']
        if not book.douban_url:
            book.douban_url = 'http://book.douban.com/subject/%s/' % data['id']
            book.douban_url = self.SUBJECT_URL.format(id=data['id'])

        try:
            img = self.download_img(data['images']['large'])
            if img:
                book.cover = Qiniu().upload(img)
                book.save()
        except Exception as e:
            logger.exception(e)
        self.update_book_tags(book, data['tags'])

    def download_img(self, url):
        resp = self.session.get(url, verify=self.verify)
        if not resp.ok:
            logger.info('get image error: %s', resp.status_code)
            return
        img = resp.content

        mime = magic.from_buffer(img, mime=True)
        if not mime.startswith('image'):
            logger.info('not image: %s, ignore', mime)
            return
        return img

    def __call__(self, book, keyword='cover_template'):
        if keyword not in book.cover:
            return

        books = self.search_book(book)
        if not books:
            return

        best_similar = self.best_match(book.name, books)
        if best_similar is None:
            return

        self.update(book, best_similar.book)
        return book

    def get_book_tags(self, book,
                      url_base='https://api.douban.com/v2/book/{id}'):
        """从豆瓣获取书籍 tags"""
        if not book.douban_url:
            return []

        douban_id = book.douban_url.split('/')[-2]
        url = url_base.format(id=douban_id)
        params = {}
        if settings.DOUBAN_APIKEY:
            params['apikey'] = settings.DOUBAN_APIKEY
        logger.debug('url: %s, params: %s', url, params)
        response = self.session.get(url, params=params, verify=self.verify)
        logger.debug('response: %s', response)
        result = response.json()
        return result['tags']

    def update_book_tags(self, book, tags=None):
        if tags is None:
            tags = self.get_book_tags(book)
        for tag in tags:
            name = tag['name']
            instance, _ = Tag.objects.get_or_create(name=name)
            if not book.tags.filter(pk=instance.pk).exists():
                book.tags.add(instance)
        return book


def update_books(sleep_days=8, recent_days=10, filter_kwargs=None):
    def _update(filter_kwargs):
        if filter_kwargs is None:
            min_read_at = now() - datetime.timedelta(recent_days)
            filter_kwargs = {
                'last_read_at__gte': min_read_at
            }
        updater = UpdateBookInfoFromDouban()
        for book in Book.objects.filter(**filter_kwargs):
            updater(book)
            logger.debug(unicode(book))
            time.sleep(60 / 10)

    while True:
        _update(filter_kwargs)
        logger.debug('sleep %s days', sleep_days)
        time.sleep(60 * 60 * 24 * sleep_days)
