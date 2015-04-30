#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from rest_framework import pagination
from rest_framework.utils.urls import replace_query_param
from rest_framework.views import Response


class LinkHeaderPagination(pagination.PageNumberPagination):
    page_size_query_param = 'per_page'
    max_page_size = 100

    def get_paginated_response(self, data):

        def page_url(page_number):
            url = self.request.build_absolute_uri()
            return replace_query_param(url, self.page_query_param, page_number)

        first_url = page_url(1) if self.page.number != 1 else None
        next_url = self.get_next_link()
        previous_url = self.get_previous_link()
        last = self.page.paginator.num_pages
        last_url = page_url(last) if last != 1 else None

        links = []
        if first_url:
            links.append('<%s>; rel="first"' % first_url)
        if previous_url:
            links.append('<%s>; rel="prev"' % previous_url)
        if next_url:
            links.append('<%s>; rel="next"' % next_url)
        if last_url:
            links.append('<%s>; rel="last"' % last_url)

        link_value = ', '.join(links)

        headers = {'Link': link_value} if link_value else {}

        return Response(data, headers=headers)
