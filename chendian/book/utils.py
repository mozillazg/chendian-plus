#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from collections import namedtuple
from difflib import SequenceMatcher

from django.conf import settings
import requests

from core.storage import Qiniu


def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()


class FetchBookInfoFromDouban(object):
    def __init__(self, book):
        self.book = book
        self.session = requests.Session()
        self.session.headers.update({
            'Connection': 'keep-alive',
            'Cache-Control': 'max-age=0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',  # noqa
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2300.0 Iron/43.0.2300.0 Safari/537.36',  # noqa
            'DNT': '1',
            'Accept-Encoding': 'gzip, deflate, sdch',
            'Accept-Language': 'en-US,en;q=0.8,zh-CN;q=0.6,zh;q=0.4',
        })
        self.session.get('http://www.douban.com')

    def search_book(self):
        url = 'https://api.douban.com/v2/book/search'
        params = {
            'q': self.book.name,
        }
        if settings.DOUBAN_APIKEY:
            params['apikey'] = settings.DOUBAN_APIKEY
        books = self.session.get(url, params=params).json()['books']
        return books

    def best_match(self, books):
        name = self.book.name
        match = namedtuple('Match', ['book', 'rate'])
        similar_rates = [
            match(book, similar(name, book['title']))
            for book in books
        ]
        min_rate = 0.5
        best_similar = similar_rates[0]
        for item in similar_rates:
            if item.rate > best_similar.rate > min_rate:
                best_similar = item
        if best_similar.rate < min_rate:
            return
        else:
            return best_similar

    def update(self, data):
        book = self.book
        if not book.author:
            book.author = ', '.join(data['author'])
        if not book.isbn:
            book.isbn = data.get('isbn13', '')
        if (not book.description) or book.description == book.name:
            book.description = data['summary']
        if not book.douban_url:
            book.douban_url = 'http://book.douban.com/subject/%s/' % data['id']

        img = self.session.get(data['images']['large']).content
        book.cover = Qiniu().upload(img)

        book.save()

    def __call__(self):
        if 'cover_template' not in self.book.cover:
            return

        books = self.search_book()
        if not books:
            return
        best_similar = self.best_match(books)
        if best_similar is None:
            return
        self.update(best_similar.book)
