#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""成员信息"""

from __future__ import absolute_import, print_function, unicode_literals

from django.views.generic import ListView

from member.models import Member


class MemberListView(ListView):
    context_object_name = 'members'
    template_name = 'member/index.html'
    paginate_by = 15

    def get_queryset(self):
        sort = self.request.GET.get('sort', 'sn')
        kwargs = {}
        filter_by = self.request.GET.get('filter_by')
        value = self.request.GET.get('filter_value')
        if filter_by in ['sn', 'qq', 'nick_name'] and value:
            if filter_by == 'nick_name':
                kwargs['nick_name__contains'] = value
            elif filter_by == 'sn':
                if value.isdigit():
                    kwargs[filter_by] = value
            else:
                kwargs[filter_by] = value

        queryset = Member.objects.filter(**kwargs)
        if sort and sort.lstrip('-') in [
            'sn', 'nick_name', 'qq'
        ]:
            queryset = queryset.order_by(sort)
        return queryset
