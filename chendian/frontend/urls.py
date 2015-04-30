#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from django.conf.urls import patterns, url
from django.contrib.auth.decorators import permission_required

from .views.book import BookDetail, BookList
from .views.member import MemberList, MemberDetail


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
        r'^m/$',
        permission_required('member.member_add', login_url=login_url)(
            MemberList.as_view()
        ),
        name='member_list'
    ),
    url(
        r'^m/(?P<pk>\d+)/$',
        permission_required('member.member_add', login_url=login_url)(
            MemberDetail.as_view()
        ),
        name='member_detail'
    ),
)
