#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required

from .views.book import BookDetail, BookList
from .views.member import MemberList, MemberDetail, member_sn


urlpatterns = patterns(
    '',
    url(
        r'^$', login_required()(BookList.as_view()),
        name='book_list'
    ),
    url(
        r'^b/$', login_required()(BookList.as_view()),
        name='book_list'
    ),
    url(
        r'^b/(?P<pk>\d+)/$', login_required()(BookDetail.as_view()),
        name='book_detail'
    ),
    url(
        r'^m/$', login_required()(MemberList.as_view()),
        name='member_list'
    ),
    url(
        r'^m/(?P<pk>\d+)/$', login_required()(MemberDetail.as_view()),
        name='member_detail'
    ),
    url(r'^m/sn/(?P<sn>\d+)/$', login_required()(member_sn), name='member_sn'),
)
