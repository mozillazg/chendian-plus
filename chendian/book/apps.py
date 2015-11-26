#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from django.apps import AppConfig
import watson


class BookConfig(AppConfig):
    name = 'book'

    def ready(self):
        Book = self.get_model("Book")
        watson.register(Book, fields=['isbn', 'name', 'author', 'tags__name'])
