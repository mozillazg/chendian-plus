#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView

from .views.book import BookDetail, BookList, book_name
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
    url(r'^b/name/(?P<name>[^/]+)/$', login_required()(book_name),
        name='book_name'),
    url(
        r'^m/$', login_required()(MemberList.as_view()),
        name='member_list'
    ),
    url(
        r'^m/(?P<pk>\d+)/$', login_required()(MemberDetail.as_view()),
        name='member_detail'
    ),
    url(r'^m/sn/(?P<sn>\d+)/$', login_required()(member_sn), name='member_sn'),

    url(
        r'^feedback/$', TemplateView.as_view(
            template_name='frontend/feedback.html'
        ),
        name='feedback'
    ),
)
