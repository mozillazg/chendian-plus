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
    get = QueryDict(request.GET.urlencode().encode('utf8'), mutable=True)
    if page_keyword in get:
        get.pop(page_keyword)
    # 除 page 参数外的其他参数
    extra_param = get.urlencode()
    if extra_param:
        extra_param = '&' + extra_param

    return "{url}?{page_keyword}={page_number}{extra_param}".format(
        url=url, page_keyword=page_keyword, page_number=page_number,
        extra_param=extra_param
    )


@register.assignment_tag(takes_context=True)
def sort_url_obj(context, value, param_name='sort'):
    """生成排序的 url 对象"""
    request = context['request']
    url = request.path
    query_dict = QueryDict(
        request.GET.urlencode().encode('utf8'), mutable=True
    )

    # 更换排序顺序
    keyword = query_dict.get(param_name, '')
    if param_name in query_dict:
        query_dict.pop(param_name)
    sorting = ''  # 当前的排序情况
    new_keyword = '-' + value
    if keyword == ('-' + value):
        sorting = 'desc'
        new_keyword = value
    elif keyword == value:
        sorting = 'asc'

    # 新的 url
    extra_param = query_dict.urlencode()
    if extra_param:
        extra_param = '&' + extra_param
    new_url = "{url}?{param_name}={new_keyword}{extra_param}".format(
        url=url, param_name=param_name, new_keyword=new_keyword,
        extra_param=extra_param
    )

    return {'new_url': new_url, 'sorting': sorting}
