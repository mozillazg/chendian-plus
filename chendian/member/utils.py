#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from core.utils import as_utc
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
    records = list(get_checkins_by_day(**kwargs))
    records.sort(key=lambda x: x.date)
    handled_dates = set()

    for record in records:
        date = record.date
        if date in handled_dates:
            continue

        date = as_utc(date)
        last_item = CheckinCount.objects.filter(
            member=member, checkined_at__lt=date
        ).order_by('checkined_at').last()

        if last_item is not None and \
                (date - last_item.checkined_at).days == 1:
            count = last_item.count + 1
        else:
            count = 1

        CheckinCount.objects.update_or_create(
            member=member, checkined_at=date,
            defaults={'count': count}
        )
        handled_dates.add(date)
