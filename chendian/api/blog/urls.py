#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from django.conf.urls import patterns
from rest_framework import routers

from .views import (
    TagViewSet, CategoryViewSet, ArticleViewSet
)

router = routers.SimpleRouter()
router.register(r'tags', TagViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'articles', ArticleViewSet)

urlpatterns = patterns(
    '',
)
urlpatterns += router.urls
