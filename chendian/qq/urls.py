#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from django.conf.urls import patterns, url

from .views.record import CheckinListView
from .views.analysis import GroupBySNListView
from .views.import_data import UploadRecordList, upload

urlpatterns = patterns(
    '',
    url(r'^records/checkins/$', CheckinListView.as_view(),
        name='record_checkin_list'),
)

urlpatterns += patterns(
    '',
    url(r'^analysis/group-by-sn/$', GroupBySNListView.as_view(),
        name='analysis_group_by_sn_list'),
)

urlpatterns += patterns(
    '',
    url(r'^imports/$', UploadRecordList.as_view(), name='import_list'),
    url(r'^imports/upload$', upload, name='upload'),
)
