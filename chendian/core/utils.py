#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

import datetime

import pytz
import times

from django.conf import settings


def str_to_local(s, format_str='%Y-%m-%d %H:%M:%S'):
    """本地日期字符串转化为本地 datetime"""
    return datetime.datetime.strptime(s, format_str)


def str_to_utc(s, format_str='%Y-%m-%d %H:%M:%S',
               timezone=settings.TIME_ZONE):
    """本地日期字符串转化为 UTC datetime"""
    d = str_to_local(s, format_str)
    return times.to_universal(d, timezone).replace(tzinfo=pytz.UTC)
