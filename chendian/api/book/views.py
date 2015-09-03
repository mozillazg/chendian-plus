#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from rest_framework.generics import (
    ListAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
)

from api._base import OnlyFieldsModelViewMixin, ExcludeFieldsModelViewMixin
from api.qq.serializers import CheckinSerializer
from book.models import Book
from qq.models import CheckinRecord
from .serializers import BookSerializer


class BookList(ExcludeFieldsModelViewMixin,
               OnlyFieldsModelViewMixin,
               ListCreateAPIView):
    model = Book
    queryset = Book.objects.all().order_by('-last_read_at')
    serializer_class = BookSerializer
    fields = [x.field_name for x in serializer_class()._readable_fields]

    def get_queryset(self):
        queryset = super(BookList, self).get_queryset()
        kwargs = {}
        name = self.request.GET.get('name', '').strip()
        if name:
            kwargs['name__icontains'] = name
        return queryset.filter(**kwargs)


class BookDetail(RetrieveUpdateDestroyAPIView):
    model = Book
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class CheckinList(ListAPIView):
    model = CheckinRecord
    queryset = CheckinRecord.sorted_objects.all()
    serializer_class = CheckinSerializer

    def get_queryset(self):
        queryset = super(CheckinList, self).get_queryset()
        book = Book.objects.filter(id=self.kwargs['book_id']).first()
        if book is None:
            return self.model.objects.none()
        return queryset.filter(book_name=book.name)


class ThinkList(CheckinList):

    def get_queryset(self):
        queryset = super(ThinkList, self).get_queryset()
        return queryset.exclude(think='')
