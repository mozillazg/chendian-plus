#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from django.views.generic.base import TemplateView


class ArticleList(TemplateView):
    template_name = 'frontend/blog/article.html'
