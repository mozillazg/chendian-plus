#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals
import datetime

from qq.models import CheckinRecord
from .models import CheckinCount


def get_checkins_by_day(**kwargs):
    queryset = CheckinRecord.objects.filter(**kwargs)
    queryset = queryset.extra(select={
        'date': "date_trunc('day', posted_at::TIMESTAMPTZ AT TIME ZONE '+08:00'::INTERVAL) "  # noqa
    }).order_by('date')
    return queryset


def update_member_checkincount(member, **kwargs):
    kwargs['qq'] = member.qq
    queryset = get_checkins_by_day(**kwargs)
    last_date = None
    last_count = 0
    for record in queryset:
        date = record.date
        if last_date is None or \
                (last_date + datetime.timedelta(days=1)) == date:
            count = last_count = last_count + 1
        else:
            count = last_count = 1
        last_date = date

        obj, _ = CheckinCount.objects.get_or_create(
            member=member, checkined_at=date
        )
        obj.count = count
        obj.save()
