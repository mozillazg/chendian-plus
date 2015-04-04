#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from django.conf.urls import patterns, url, include

urlpatterns = patterns(
    '',
    url(r'^qq/', include('api.qq.urls', namespace='qq')),
    url(r'^members/', include('api.member.urls', namespace='member')),
    url(r'^books/', include('api.book.urls', namespace='book')),
)
