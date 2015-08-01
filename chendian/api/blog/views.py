#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from rest_framework.viewsets import ReadOnlyModelViewSet

from api._base import CreateListRetrieveViewSet
from blog.models import Article, Tag, Category
from .serializers import ArticleSerializer, TagSerializer, CategorySerializer


class CategoryViewSet(ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    search_fields = ('name',)
    filter_fields = ('id',)


class TagViewSet(ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    search_fields = ('name',)
    filter_fields = ('id',)


class ArticleViewSet(CreateListRetrieveViewSet):
    queryset = Article.objects.filter(status=Article.STATUS_APPROVED)
    serializer_class = ArticleSerializer
    filter_fields = (
        'id', 'author__nick_name',
        'categories__slug', 'tags__slug'
    )
    search_fields = ('title',)
