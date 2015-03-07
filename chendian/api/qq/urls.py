#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from django.conf.urls import patterns, url

from .record import CheckinList, CheckinDetail

urlpatterns = patterns(
    '',
    url(r'^checkins/$', CheckinList.as_view(),
        name='checkin_list'),
    url(r'^checkins/(?P<pk>\d+)/$', CheckinDetail.as_view(),
        name='checkin_detail'),
)
