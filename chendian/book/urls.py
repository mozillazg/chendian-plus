#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from django.conf.urls import patterns, url
from django.contrib.auth.decorators import permission_required

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
)
