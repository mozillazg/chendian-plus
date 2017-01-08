#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from django.conf.urls import patterns, url

from .views import (
    MemberList, MemberDetail, NewMemberApprove, CheckinList, BookList,
    CheckinCountsView, YearBookList, YearBookCount
)

urlpatterns = patterns(
    '',
    url(r'^$', MemberList.as_view(),
        name='member_list'),
    url(r'^(?P<pk>\d+)/$', MemberDetail.as_view(),
        name='member_detail'),
    url(r'^new_member/(?P<pk>\d+)/approve/$', NewMemberApprove.as_view(),
        name='new_member_approve'),

    url(r'^(?P<pk>\d+)/checkins/$', CheckinList.as_view(),
        name='checkin_list'),
    url(r'^(?P<pk>\d+)/checkin-counts/$', CheckinCountsView.as_view(),
        name='checkin_counts'),
    url(r'^(?P<pk>\d+)/checkin-counts/(?P<year>20\d\d)/$',
        CheckinCountsView.as_view(), name='checkin_counts_year'),

    url(r'^(?P<pk>\d+)/books/$', BookList.as_view(),
        name='book_list'),

    url(r'^(?P<pk>\d+)/year/(?P<year>2\d{3})/books/count$',
        YearBookCount.as_view(), name='year_book_count'),
    url(r'^(?P<pk>\d+)/year/(?P<year>2\d{3})/books/$', YearBookList.as_view(),
        name='year_book_list'),
)
