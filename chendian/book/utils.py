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


def update_books(sleep_days=8, recent_days=10, filter_kwargs=None):
    def _update(filter_kwargs):
        if filter_kwargs is None:
            min_read_at = now() - datetime.timedelta(recent_days)
            filter_kwargs = {
                'last_read_at__gte': min_read_at
            }
        updater = UpdateBookInfoFromDouban()
        for book in Book.objects.filter(**filter_kwargs):
            result = updater(book)
            logger.debug(unicode(book))
            if result is not None:
                time.sleep(60 / 8)

    while 1:
        _update(filter_kwargs)
        logger.debug('sleep %s days', sleep_days)
        time.sleep(60 * 60 * 24 * sleep_days)
