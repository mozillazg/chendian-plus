#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from django.conf.urls import patterns, url
from django.contrib.auth.decorators import permission_required

from .views.account import UserInfo
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
        r'^b/$',
        permission_required('book.book', login_url=login_url)(
            BookList.as_view()
        ),
        name='book_list'
    ),
    url(
        r'^b/(?P<pk>\d+)/$',
        permission_required('book.book', login_url=login_url)(
            BookDetail.as_view()
        ),
        name='book_detail'
    ),
    url(
        r'^u/(?P<pk>\d+)/$',
        permission_required('user.user_add', login_url=login_url)(
            UserInfo.as_view()
        ),
        name='user_info'
    ),
)
