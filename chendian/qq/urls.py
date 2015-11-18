#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals
import functools

from django.conf.urls import patterns, url
from django.contrib.admin.views.decorators import staff_member_required

from .views.record import CheckinListView
from .views.analysis import GroupByQQListView
from .views.import_data import UploadRecordList, upload

login_url = 'login'
staff_member_required = functools.partial(
    staff_member_required, login_url=login_url
)

urlpatterns = patterns(
    '',
    url(
        r'^records/checkins/$',
        staff_member_required(CheckinListView.as_view()),
        name='record_checkin_list'
    ),
)

urlpatterns += patterns(
    '',
    url(
        r'^analysis/group-by-qq/$',
        staff_member_required(GroupByQQListView.as_view()),
        name='analysis_group_by_qq_list'
    ),
)

urlpatterns += patterns(
    '',
    url(
        r'^imports/$',
        staff_member_required(UploadRecordList.as_view()),
        name='import_list'
    ),
    url(r'^imports/upload$', staff_member_required(upload), name='upload'),
)
