#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals
import calendar


def fill_calendar_for_count(year, data, default=0):
    days = {x['date'] for x in data}
    for month in xrange(1, 13):
        for d in xrange(1, calendar.monthrange(year, month)[1]+1):
            day = '{0}-{1:0>2}-{2:0>2}'.format(year, month, d)
            if day in days:
                continue
            else:
                data.append({'date': day, 'count': default})

    data.sort(key=lambda x: x['date'])
