#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals
import functools

from django.conf.urls import patterns, url
from django.contrib.admin.views.decorators import staff_member_required

from .views import MemberListView, NewMemberListView

login_url = 'login'
staff_member_required = functools.partial(
    staff_member_required, login_url=login_url
)

urlpatterns = patterns(
    '',
    url(
        r'^$', staff_member_required(MemberListView.as_view()),
        name='member_list'
    ),
    url(
        r'^new/$',
        staff_member_required(NewMemberListView.as_view()),
        name='new_member_list'
    ),
)
