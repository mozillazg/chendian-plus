#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from rest_framework.generics import (
    ListCreateAPIView, RetrieveUpdateDestroyAPIView
)
from rest_framework.viewsets import ReadOnlyModelViewSet

from blog.models import Article, Tag, Category
from .serializers import ArticleSerializer, TagSerializer, CategorySerializer


class CategoryViewSet(ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class TagViewSet(ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


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
