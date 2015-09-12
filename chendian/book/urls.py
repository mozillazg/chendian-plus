#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from django.conf.urls import patterns, url
from django.contrib.auth.decorators import permission_required

from qq.views.index import HomeListView
from .views import BookListView

login_url = 'login'

urlpatterns = patterns(
    '',
    url(
        r'^$',
        permission_required('book.book', login_url=login_url)(
            BookListView.as_view()
        ),
        name='book_list'
    ),
    url(
        r'^hot/$',
        permission_required('book.book', login_url=login_url)(
            HomeListView.as_view()
        ),
        name='book_hot'
    ),
)
