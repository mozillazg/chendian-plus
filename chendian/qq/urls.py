#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from django.conf.urls import patterns, url
from django.contrib.auth.decorators import permission_required

from .views.record import CheckinListView
from .views.analysis import GroupByQQListView
from .views.import_data import UploadRecordList, upload

login_url = 'login'

urlpatterns = patterns(
    '',
    url(
        r'^records/checkins/$',
        permission_required('qq.checkinrecord_add', login_url=login_url)(
            CheckinListView.as_view()
        ),
        name='record_checkin_list'
    ),
)

urlpatterns += patterns(
    '',
    url(
        r'^analysis/group-by-qq/$',
        permission_required('qq.checkinrecord_add', login_url=login_url)(
            GroupByQQListView.as_view()
        ),
        name='analysis_group_by_qq_list'
    ),
)

urlpatterns += patterns(
    '',
    url(
        r'^imports/$',
        permission_required('qq.checkinrecord_add', login_url=login_url)(
            UploadRecordList.as_view()
        ),
        name='import_list'
    ),
    url(
        r'^imports/upload$',
        permission_required('qq.checkinrecord_add', login_url=login_url)(
            upload
        ),
        name='upload'
    ),
)
