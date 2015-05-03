#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from django.core.urlresolvers import reverse_lazy
from django.http import Http404, HttpResponseRedirect
from django.views.generic.base import TemplateView

from book.models import Book


class BookList(TemplateView):
    template_name = 'frontend/book/index.html'


class BookDetail(TemplateView):
    template_name = 'frontend/book/detail.html'

    def get_context_data(self, **kwargs):
        context = super(BookDetail, self).get_context_data(**kwargs)
        context['id'] = self.kwargs['pk']
        return context


def book_name(request, name):
    book = Book.objects.filter(name=name).first()
    if book is None:
        raise Http404()
    return HttpResponseRedirect(
        reverse_lazy('frontend:book_detail', kwargs={'pk': book.pk})
    )
