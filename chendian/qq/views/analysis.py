#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from django.db.models import Count
from django.views.generic import ListView

from core.utils import (
    str_to_utc, default_datetime_start, default_datetime_end
)
from qq.models import CheckinRecord


class GroupBySNListView(ListView):
    context_object_name = 'records'
    template_name = 'qq/analysis/group_by_sn.html'
    paginate_by = 15

    def get_queryset(self):
        sort = self.request.GET.get('sort')
        filter_by = self.request.GET.get('filter_by')
        filter_value = self.request.GET.get('filter_value')
        datetime_start = str_to_utc(
            self.request.GET.get('datetime_start', '') + ':00',
            default=default_datetime_start
        )
        datetime_end = str_to_utc(
            self.request.GET.get('datetime_end', '') + ':00',
            default=default_datetime_end
        )
        self.extra_context = {
            'datetime_start': datetime_start,
            'datetime_end': datetime_end,
        }
        kwargs = {}
        if filter_value:
            if filter_by == 'sn':
                if filter_value.isdigit():
                    kwargs['sn'] = filter_value
            elif filter_by == 'nick_name':
                kwargs['nick_name__contains'] = filter_value
            elif filter_by == 'qq':
                kwargs['qq'] = filter_value
        if datetime_start:
            kwargs['posted_at__gte'] = datetime_start
        if datetime_end:
            kwargs['posted_at__lte'] = datetime_end

        queryset = CheckinRecord.objects.filter(**kwargs)
        queryset = queryset.values('sn', 'nick_name').annotate(
            count=Count('pk')
        )
        if sort:
            queryset = queryset.order_by(sort)
        return queryset

    def get_context_data(self, **kwargs):
        context = super(GroupBySNListView, self).get_context_data(**kwargs)
        context.update(self.extra_context)
        return context
