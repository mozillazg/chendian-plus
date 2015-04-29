#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from django.conf.urls import patterns, url

from .views import BookList, BookDetail, ThinkList

urlpatterns = patterns(
    '',
    url(r'^$', BookList.as_view(), name='book_list'),
    url(r'^(?P<pk>\d+)/$', BookDetail.as_view(), name='book_detail'),
    url(r'^(?P<book_id>\d+)/thinks/$', ThinkList.as_view(), name='think_list'),
)
