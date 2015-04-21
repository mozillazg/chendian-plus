#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""统计分析"""

from __future__ import absolute_import, print_function, unicode_literals

from collections import OrderedDict
import logging

from django.views.generic import ListView

from core.aggregates import CountWithFunc
from core.utils import xlsx_response
from qq.models import CheckinRecord
from qq.utils import record_filter_kwargs

logger = logging.getLogger(__name__)


class GroupByQQListView(ListView):
    context_object_name = 'records'
    template_name = 'qq/analysis/group_by_qq.html'
    paginate_by = 50

    def get_queryset(self):
        sort = self.request.GET.get('sort', '-count')
        kwargs = record_filter_kwargs(self.request)
        self.extra_context = {
            'datetime_start': kwargs['posted_at__gte'],
            'datetime_end': kwargs['posted_at__lte'],
            'book_name': kwargs.get('book_name', ''),
        }
        kwargs.update({'deleted': False})

        queryset = CheckinRecord.objects.filter(**kwargs)
        queryset = queryset.values(
            'sn', 'qq', 'nick_name'
        ).annotate(
            count=CountWithFunc(
                "date_trunc('day', posted_at::TIMESTAMPTZ AT TIME ZONE "
                "'+08:00'::INTERVAL)",
                distinct=True
            )
        )
        logger.debug(queryset.query)
        if sort and sort.lstrip('-') in ['sn', 'nick_name', 'qq', 'count']:
            queryset = queryset.order_by(sort)
        return queryset

    def get_context_data(self, **kwargs):
        context = super(GroupByQQListView, self).get_context_data(**kwargs)
        context.update(self.extra_context)
        return context

    def render_to_response(self, context, **response_kwargs):
        if self.request.GET.get('export') != 'xlsx':
            return super(GroupByQQListView, self).render_to_response(
                context, **response_kwargs
            )

        queryset = self.get_queryset()
        xlsx_headers = OrderedDict([
            ('编号', 'sn'),
            ('昵称', 'nick_name'),
            ('QQ', 'qq'),
            ('打卡天数', 'count'),
        ])
        filename = u'%s-%s打卡情况' % (
            self.extra_context['datetime_start'],
            self.extra_context['datetime_end']
        )
        return xlsx_response(xlsx_headers, queryset, filename)
