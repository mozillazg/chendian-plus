#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from django import template
from django.http import QueryDict

register = template.Library()


@register.simple_tag(takes_context=True)
def page_url(context, page_number, page_keyword="page"):
    request = context['request']
    url = request.path
    get = QueryDict(request.GET.urlencode(), mutable=True)
    if page_keyword in get:
        get.pop(page_keyword)
    extra_param = get.urlencode()
    if extra_param:
        extra_param = '&' + extra_param

    return "{url}?{page_keyword}={page_number}{extra_param}".format(
        url=url, page_keyword=page_keyword, page_number=page_number,
        extra_param=extra_param
    )
