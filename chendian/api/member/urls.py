#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from django.conf.urls import patterns, url

from .views import MemberList, MemberDetail, NewMemberApprove

urlpatterns = patterns(
    '',
    url(r'^$', MemberList.as_view(),
        name='member_list'),
    url(r'^(?P<pk>\d+)/$', MemberDetail.as_view(),
        name='member_detail'),
    url(r'^new_member/(?P<pk>\d+)/approve/$', NewMemberApprove.as_view(),
        name='new_member_approve'),
)
