#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from django.views.generic.base import TemplateView


class BookList(TemplateView):
    template_name = 'frontend/book/index.html'


class BookDetail(TemplateView):
    template_name = 'frontend/book/detail.html'

    def get_context_data(self, **kwargs):
        context = super(BookDetail, self).get_context_data(**kwargs)
        context['id'] = self.kwargs['pk']
        return context
