#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from django.conf import settings
from django.conf.urls import patterns, url
from django.views.generic import TemplateView
from django.views.generic.base import RedirectView

from .views.blog import ArticleList, ArticleDetail
from .views.book import BookDetail, BookList, book_name
from .views.member import MemberList, MemberDetail, member_sn


urlpatterns = patterns(
    '',
    url(
        r'^$', RedirectView.as_view(url=settings.HOME_URI, permanent=False),
        name='blog_home'
    ),

    # 文章
    url(r'^a/$', ArticleList.as_view(), name='article_list'),
    url(r'^a/(?P<pk>\d+)/$', ArticleDetail.as_view(), name='article_detail'),

    # 书籍
    url(r'^b/$', BookList.as_view(), name='book_list'),
    url(r'^b/(?P<pk>\d+)/$', BookDetail.as_view(), name='book_detail'),
    url(r'^b/name/(?P<name>[^/]{2,50})/$', book_name, name='book_name'),

    # 成员
    url(r'^m/$', MemberList.as_view(), name='member_list'),
    url(r'^m/(?P<pk>\d+)/$', MemberDetail.as_view(), name='member_detail'),
    url(r'^m/sn/(?P<sn>\d+)/$', member_sn, name='member_sn'),

    # 吐槽
    url(
        r'^feedback/$', TemplateView.as_view(
            template_name='frontend/feedback.html'
        ),
        name='feedback'
    ),

    url(
        r'^(?P<year>2\d{3})/$', TemplateView.as_view(
            template_name='frontend/year_summarize.html'
        ),
        name='year_summarize'
    ),
)
