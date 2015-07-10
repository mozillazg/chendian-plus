#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from django.conf.urls import patterns, url
from rest_framework import routers

from .views import TagViewSet, CategoryViewSet, ArticleList, ArticleDetail

router = routers.SimpleRouter()
router.register(r'tags', TagViewSet)
router.register(r'categories', CategoryViewSet)

urlpatterns = patterns(
    '',
    url(r'^articles/$', ArticleList.as_view(), name='article_list'),
    url(r'^articles/(?P<pk>\d+)/$', ArticleDetail.as_view(),
        name='article_detail'),
)
urlpatterns += router.urls
