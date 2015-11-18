#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals
import functools

from django.conf.urls import patterns, url
from django.contrib.admin.views.decorators import staff_member_required

from qq.views.index import HomeListView
from .views import BookListView

login_url = 'login'
staff_member_required = functools.partial(
    staff_member_required, login_url=login_url
)

urlpatterns = patterns(
    '',
    url(
        r'^$', staff_member_required(BookListView.as_view()), name='book_list'
    ),
    url(
        r'^hot/$', staff_member_required(HomeListView.as_view()),
        name='book_hot'
    ),
)
