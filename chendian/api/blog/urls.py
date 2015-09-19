#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from django.conf.urls import patterns, url
from rest_framework import routers

from .views import (
    TagViewSet, CategoryViewSet, ArticleViewSet, ArticleApprove
)

router = routers.SimpleRouter()
router.register(r'tags', TagViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'articles', ArticleViewSet)

urlpatterns = patterns(
    '',
    url('^articles/(?P<pk>\d+)/approve/$', ArticleApprove.as_view(),
        name='article_approve'),
)
urlpatterns += router.urls
