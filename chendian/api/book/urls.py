#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from django.conf.urls import patterns, url

from .views import (
    BookList, BookDetail, ThinkList, CheckinList, HundredGoalNoteList,
    TagList, TagNew, BookYearCount, BooksYearTopList
)

urlpatterns = patterns(
    '',
    url(r'^$', BookList.as_view(), name='book_list'),
    url(r'^(?P<pk>\d+)/$', BookDetail.as_view(), name='book_detail'),
    url(r'^(?P<book_id>\d+)/checkins/$', CheckinList.as_view(),
        name='checkin_list'),
    url(r'^(?P<book_id>\d+)/thinks/$', ThinkList.as_view(), name='think_list'),
    url(r'^(?P<book_id>\d+)/hundred-goal-notes/$',
        HundredGoalNoteList.as_view(), name='handred_goal_note_list'),
    url(r'^(?P<book_id>\d+)/tags/$', TagList.as_view(),
        name='book_tag_list'),
    url(r'^(?P<book_id>\d+)/tags/new$', TagNew.as_view(),
        name='book_tag_new'),

    url(r'^(?P<book_id>\d+)/year/(?P<year>2\d{3})/count$',
        BookYearCount.as_view(), name='book_year_count'),
    url(r'^year/(?P<year>2\d{3})/top/(?P<top>(\d{1,2}|100))/$',
        BooksYearTopList.as_view(), name='books_year_top'),
)
