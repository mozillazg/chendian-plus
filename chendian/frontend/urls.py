#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from django.conf.urls import patterns, url
from django.contrib.auth.decorators import permission_required

from .views.book import BookDetail, BookList


login_url = 'login'

urlpatterns = patterns(
    '',
    url(
        r'^$',
        permission_required('book.book', login_url=login_url)(
            BookList.as_view()
        ),
        name='book_list'
    ),
    url(
        r'^books/$',
        permission_required('book.book', login_url=login_url)(
            BookList.as_view()
        ),
        name='book_list'
    ),
    url(
        r'^books/(?P<pk>\d+)/$',
        permission_required('book.book', login_url=login_url)(
            BookDetail.as_view()
        ),
        name='book_detail'
    ),
)
