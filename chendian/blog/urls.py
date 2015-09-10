#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from django.conf.urls import patterns, url
from django.contrib.auth.decorators import permission_required

from .views import ArticleListView

login_url = 'login'

urlpatterns = patterns(
    '',
    url(
        r'^articles/$',
        permission_required('blog.article', login_url=login_url)(
            ArticleListView.as_view()
        ),
        name='article_list'
    ),
)
