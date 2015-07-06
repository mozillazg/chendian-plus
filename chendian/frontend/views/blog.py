#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from django.views.generic.base import TemplateView


class ArticleList(TemplateView):
    template_name = 'frontend/blog/article_list.html'


class ArticleDetail(TemplateView):
    template_name = 'frontend/blog/article_detail.html'

    def get_context_data(self, **kwargs):
        context = super(ArticleDetail, self).get_context_data(**kwargs)
        context['id'] = self.kwargs['pk']
        return context
