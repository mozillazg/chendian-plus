#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from rest_framework.generics import (
    ListCreateAPIView, RetrieveUpdateDestroyAPIView
)

from blog.models import Article
from .serializers import ArticleSerializer


class ArticleList(ListCreateAPIView):
    model = Article
    queryset = Article.objects.filter(status=Article.STATUS_APPROVED)
    serializer_class = ArticleSerializer
    filter_fields = (
        'id', 'author__nick_name',
        'categories__slug', 'tags__slug'
    )

    def get_queryset(self):
        queryset = super(ArticleList, self).get_queryset()
        kwargs = {}
        title = self.request.GET.get('title', '').strip()
        if title:
            kwargs['title__icontains'] = title
        return queryset.filter(**kwargs)


class ArticleDetail(RetrieveUpdateDestroyAPIView):
    model = Article
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
