#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals
import functools

from django.conf.urls import patterns, url
from django.contrib.admin.views.decorators import staff_member_required

from .views import ArticleListView, TagListView, CategoryListView

login_url = 'login'
staff_member_required = functools.partial(
    staff_member_required, login_url=login_url
)

urlpatterns = patterns(
    '',
    url(
        r'^articles/$',
        staff_member_required(ArticleListView.as_view()),
        name='article_list'
    ),
    url(
        r'^tags/$',
        staff_member_required(TagListView.as_view()),
        name='tag_list'
    ),
    url(
        r'^categories/$',
        staff_member_required(CategoryListView.as_view()),
        name='category_list'
    ),
)
