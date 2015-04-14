#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from collections import OrderedDict
import datetime
from StringIO import StringIO

from pyexcel_xlsx import XLSXWriter
import pytz
import times

from django.conf import settings
from django.http import HttpResponse


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
        return times.now().replace(tzinfo=pytz.UTC) - datetime.timedelta(days=31)
    return datetime_end - datetime.timedelta(days=31)


def default_datetime_end(datetime_start=None):
    if not datetime_start:
        return times.now().replace(tzinfo=pytz.UTC)
    return datetime_start + datetime.timedelta(days=31)


def data2xlsx(headers, data, sheet_name='Sheet 1'):
    """
    :type headers: OrderedDict
    :param headers:
                    {
                        '名称': 'name',
                        'QQ': 'qq',
                     }
    """
    sheet = []
    sheets = {sheet_name: sheet}
    sheets = OrderedDict(sheets)

    sheet.extend([headers.keys()])
    for line in data:
        rows = []
        for attr in headers.values():
            if isinstance(line, dict):
                v = line.get(attr, '')
            else:
                v = getattr(line, attr, '')
            if isinstance(v, (datetime.datetime)):
                v = v.strftime('%Y-%m-%d %H:%M:%S')
            elif isinstance(v, (datetime.date)):
                v = v.strftime('%Y-%m-%d')
            elif v is None:
                v = ''
            rows.append(v)
        sheet.append(rows)

    io = StringIO()
    writer = XLSXWriter(io)
    writer.write(sheets)
    writer.close()
    return io.getvalue()


def attachment_response(data, filename, content_type):
    response = HttpResponse(content_type=content_type)
    response['Content-Disposition'] = 'attachment; filename="%s"' % filename
    response.write(data)
    return response


def xlsx_response(xlsx_headers, data, filename, sheet_name='Sheet 1'):
    content_type = (
        'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    xlsx_data = data2xlsx(xlsx_headers, data, sheet_name)
    return attachment_response(xlsx_data, filename, content_type)
