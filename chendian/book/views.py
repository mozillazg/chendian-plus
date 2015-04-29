#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from django.views.generic import ListView

from .models import Book


class BookListView(ListView):
    context_object_name = 'books'
    template_name = 'book/index.html'
    paginate_by = 50

    def get_queryset(self):
        kwargs = {}
        filter_by = self.request.GET.get('filter_by')
        value = self.request.GET.get('filter_value')
        if filter_by in ['isbn', 'name'] and value:
            if filter_by == 'name':
                kwargs['name__contains'] = value
            else:
                kwargs[filter_by] = value

        queryset = Book.objects.filter(**kwargs).order_by('-last_read_at')
        return queryset
