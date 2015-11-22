#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from rest_framework.generics import (
    ListAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
)
import watson

from api._base import OnlyFieldsModelViewMixin, ExcludeFieldsModelViewMixin
from api.qq.serializers import (
    CheckinSerializer, DynamicCheckinSerializerClass
)
from book.models import Book, HundredGoalNote
from qq.models import CheckinRecord
from .serializers import BookSerializer, HundredGoalNoteSerializer


class BookList(ExcludeFieldsModelViewMixin,
               OnlyFieldsModelViewMixin,
               ListCreateAPIView):
    model = Book
    queryset = Book.objects.all().order_by('-last_read_at')
    serializer_class = BookSerializer
    fields = [x.field_name for x in serializer_class()._readable_fields]

    def get_queryset(self):
        queryset = super(BookList, self).get_queryset()
        name = self.request.GET.get('name', '').strip()
        if name:
            pks = watson.search(name, models=(queryset,)).values_list(
                'object_id', flat=True
            )
            queryset = queryset.filter(id__in=list(pks))
        return queryset


class BookDetail(RetrieveUpdateDestroyAPIView):
    model = Book
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class CheckinList(DynamicCheckinSerializerClass, ListAPIView):
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


class HundredGoalNoteList(ListAPIView):
    model = HundredGoalNote
    serializer_class = HundredGoalNoteSerializer
    queryset = HundredGoalNote.objects.all().order_by('-id')

    def get_queryset(self):
        queryset = super(HundredGoalNoteList, self).get_queryset()
        return queryset.filter(book__id=self.kwargs['book_id'])
