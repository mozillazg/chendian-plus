#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from api.permissions import IsAdminOrReadonly, IsAdminOrReadAndCreate
from blog.models import Article, Tag, Category
from .serializers import ArticleSerializer, TagSerializer, CategorySerializer


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    search_fields = ('name',)
    filter_fields = ('id',)
    permission_classes = (IsAdminOrReadonly,)


class TagViewSet(ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    search_fields = ('name',)
    filter_fields = ('id',)


class ArticleViewSet(ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    filter_fields = (
        'id', 'author__nick_name',
        'categories__slug', 'tags__slug'
    )
    search_fields = ('title',)
    permission_classes = (IsAdminOrReadAndCreate,)

    def get_queryset(self):
        queryset = super(ArticleViewSet, self).get_queryset()
        if not self.request.user.is_staff:
            queryset = queryset.filter(status=Article.STATUS_APPROVED)

        return queryset.select_related('author'
                                       ).prefetch_related('tags',
                                                          'categories')


class ArticleApprove(APIView):
    permission_classes = (IsAdminUser,)

    def put(self, request, pk, *args, **kwargs):
        article = get_object_or_404(Article.objects.all(), pk=pk)
        article.status = Article.STATUS_APPROVED
        article.save()
        return Response(status=204)

    def delete(self, request, pk, *args, **kwargs):
        article = get_object_or_404(Article.objects.all(), pk=pk)
        article.status = Article.STATUS_DISAPPROVED
        article.save()
        return Response(status=204)
