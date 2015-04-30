#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from django.views.generic.base import TemplateView


class UserInfo(TemplateView):
    template_name = 'frontend/userinfo.html'

    def get_context_data(self, **kwargs):
        context = super(UserInfo, self).get_context_data(**kwargs)
        context['id'] = self.kwargs['pk']
        return context
