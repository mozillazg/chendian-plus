#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""打卡记录"""

from __future__ import absolute_import, print_function, unicode_literals

from django.views.generic import ListView

from qq.models import CheckinRecord
from qq.utils import record_filter_kwargs


class CheckinListView(ListView):
    context_object_name = 'records'
    template_name = 'qq/record/checkin.html'
    paginate_by = 15

    def get_queryset(self):
        sort = self.request.GET.get('sort')
        kwargs = record_filter_kwargs(self.request)
        self.extra_context = {
            'datetime_start': kwargs['posted_at__gte'],
            'datetime_end': kwargs['posted_at__lte'],
        }

        queryset = CheckinRecord.sorted_objects.filter(**kwargs)
        if sort and sort.lstrip('-') in [
            'sn', 'nick_name', 'qq', 'book_name', 'posted_at'
        ]:
            queryset = queryset.order_by(sort)
        return queryset

    def get_context_data(self, **kwargs):
        context = super(CheckinListView, self).get_context_data(**kwargs)
        context.update(self.extra_context)
        return context
