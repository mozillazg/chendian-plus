#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

import datetime

import pytz
import times

from django.conf import settings


def str_to_local(s, format_str='%Y-%m-%d %H:%M:%S', default=None):
    """本地日期字符串转化为本地 datetime"""
    try:
        return datetime.datetime.strptime(s, format_str)
    except:
        if default:
            return default
        else:
            raise


def str_to_utc(s, format_str='%Y-%m-%d %H:%M:%S',
               timezone=settings.TIME_ZONE, default=None):
    """本地日期字符串转化为 UTC datetime"""
    try:
        d = str_to_local(s, format_str)
        return times.to_universal(d, timezone).replace(tzinfo=pytz.UTC)
    except:
        if default:
            return default
        else:
            raise


def utc_to_local(utc, timezone=settings.TIME_ZONE):
    return utc.astimezone(pytz.timezone(timezone))


def default_datetime_start(datetime_end=None):
    if not datetime_end:
        return times.now().replace(tzinfo=pytz.UTC) - datetime.timedelta(days=7)
    return datetime_end - datetime.timedelta(days=7)


def default_datetime_end(datetime_start=None):
    if not datetime_start:
        return times.now().replace(tzinfo=pytz.UTC)
    return datetime_start + datetime.timedelta(days=7)
