#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

import django_filters
from django.views.generic import ListView

from .models import Article, Tag, Category


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
        queryset = queryset.select_related('author').only(
            'id', 'title', 'author', 'status', 'created_at'
        )
        queryset = ArticleFilter(self.request.GET, queryset)
        return queryset


class TagListView(ListView):
    model = Tag
    context_object_name = 'tag'
    template_name = 'blog/tag_or_category_list.html'
    paginate_by = 50


class CategoryListView(ListView):
    model = Category
    context_object_name = 'category'
    template_name = 'blog/tag_or_category_list.html'
    paginate_by = 50
