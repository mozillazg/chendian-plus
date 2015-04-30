#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from django.views.generic.base import TemplateView


class MemberList(TemplateView):
    template_name = 'frontend/member/index.html'


class MemberDetail(TemplateView):
    template_name = 'frontend/member/detail.html'

    def get_context_data(self, **kwargs):
        context = super(MemberDetail, self).get_context_data(**kwargs)
        context['id'] = self.kwargs['pk']
        return context
