#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

import django_filters
from django.views.generic import ListView

from .models import Article


class ArticleFilter(django_filters.FilterSet):
    class Meta:
        model = Article
        fields = ['id', 'status', 'sticky']


class ArticleListView(ListView):
    model = Article
    context_object_name = 'articles'
    template_name = 'blog/article_list.html'
    paginate_by = 50

    def get_queryset(self):
        queryset = super(ArticleListView, self).get_queryset()
        queryset = ArticleFilter(self.request.GET, queryset)
        return queryset
