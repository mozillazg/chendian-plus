#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from django.db.models import Count
# from django.shortcuts import render_to_response
# from django.template import RequestContext
from django.views.generic import ListView

from qq.models import CheckinRecord
from qq.utils import record_filter_kwargs
#
#
# def home(request, template_name='index.html'):
#     kwargs = record_filter_kwargs(request)
#     kwargs.update({'deleted': False})
#     books = CheckinRecord.objects.filter(**kwargs).exclude(
#         book_name=''
#     ).values('book_name').annotate(
#         count=Count('pk')
#     )
#
#     context = {
#         'books': books,
#         'datetime_start': kwargs['posted_at__gte'],
#         'datetime_end': kwargs['posted_at__lte'],
#     }
#     return render_to_response(
#         template_name, context, context_instance=RequestContext(request)
#     )


class HomeListView(ListView):
    context_object_name = 'books'
    template_name = 'index.html'
    paginate_by = 50

    def get_queryset(self):
        sort = self.request.GET.get('sort', '-count')
        kwargs = record_filter_kwargs(self.request)
        self.extra_context = {
            'datetime_start': kwargs['posted_at__gte'],
            'datetime_end': kwargs['posted_at__lte'],
        }
        kwargs.update({'deleted': False})

        queryset = CheckinRecord.objects.filter(**kwargs).exclude(
            book_name=''
        ).values('book_name').annotate(
            count=Count('qq', distinct=True)
        ).filter(count__gt=2)

        if sort and sort.lstrip('-') in ['book_name', 'count']:
            queryset = queryset.order_by(sort)
        return queryset

    def get_context_data(self, **kwargs):
        context = super(HomeListView, self).get_context_data(**kwargs)
        context.update(self.extra_context)
        return context
