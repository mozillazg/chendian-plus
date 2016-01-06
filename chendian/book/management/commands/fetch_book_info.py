#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

import datetime
import logging
import time

from django.core.management.base import BaseCommand, CommandError

from book.models import Book
from book.utils import UpdateBookInfoFromDouban

logger = logging.getLogger(__name__)


def update_book(book_id):
    book = Book.objects.get(pk=book_id)
    updater = UpdateBookInfoFromDouban(False)
    updater(book)


def update_books(days=30, **kwargs):
    gt = lambda: datetime.datetime.now() - datetime.timedelta(days)
    if not kwargs:
        kwargs = dict(cover__contains='cover')
    books = Book.objects.filter(created_at__gt=gt(), **kwargs
                                ).order_by('-last_read_at').only('id')
    for book in books:
        try:
            update_book(book.id)
        except Exception as e:
            print(e)
        finally:
            print(book.id)
            time.sleep(10)


class Command(BaseCommand):
    help = 'fetch book info from douban api'

    def add_arguments(self, parser):
        parser.add_argument('book_id', nargs='+', type=int)

    def handle(self, *args, **options):
        for book_id in options['book_id']:
            try:
                if book_id == 0:
                    update_books()
                else:
                    update_book(book_id)
            except Book.DoesNotExist:
                raise CommandError('Book "%s" does not exist' % book_id)

            self.stdout.write('Successfully updated book "%s"' % book_id)
