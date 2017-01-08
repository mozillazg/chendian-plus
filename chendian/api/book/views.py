#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from django.shortcuts import get_object_or_404
from rest_framework.generics import (
    ListAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView,
    CreateAPIView, RetrieveAPIView
)
import watson

from api._base import (
    OnlyFieldsModelViewMixin, ExcludeFieldsModelViewMixin,
    ExportMixin
)
from api.qq.serializers import (
    CheckinSerializer, DynamicCheckinSerializerClass
)
from blog.models import Tag
from book.models import Book, HundredGoalNote, YearBook
from qq.models import CheckinRecord
from .serializers import (
    BookSerializer, HundredGoalNoteSerializer, TagSerializer,
    YearBookSerializer
)


class BookList(ExcludeFieldsModelViewMixin,
               OnlyFieldsModelViewMixin,
               ListCreateAPIView):
    model = Book
    queryset = Book.objects.all().order_by('-last_read_at')
    serializer_class = BookSerializer
    fields = [x.field_name for x in serializer_class()._readable_fields]
    filter_fields = ('id', 'tags__name')

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
    queryset = HundredGoalNote.objects.all().order_by('-created_at')

    def get_queryset(self):
        queryset = super(HundredGoalNoteList, self).get_queryset()
        return queryset.filter(book__id=self.kwargs['book_id'])


class TagList(ListAPIView):
    models = Tag
    serializer_class = TagSerializer

    def get_queryset(self):
        book = get_object_or_404(Book.objects.all(), pk=self.kwargs['book_id'])
        return book.tags.all()


class TagNew(CreateAPIView):
    models = Tag
    serializer_class = TagSerializer

    def get_book(self):
        return get_object_or_404(Book.objects.all(), pk=self.kwargs['book_id'])

    def perform_create(self, serializer):
        book = self.get_book()
        tag_name = serializer.validated_data['name']
        tag = Tag.objects.filter(name=tag_name).first()
        # if tag name exists then update
        if tag is not None:
            serializer.instance = tag
        serializer.save()

        # add new tag to book
        tag = serializer.instance
        if not book.tags.filter(pk=tag.pk).exists():
            book.tags.add(tag)


class BookYearDetail(RetrieveAPIView):
    model = YearBook
    serializer_class = YearBookSerializer
    queryset = YearBook.objects.all()
    lookup_field = 'book_id'

    def get_queryset(self):
        queryset = super(BookYearDetail, self).get_queryset()
        return queryset.filter(year=self.kwargs['year'])


class BooksYearTopList(ExportMixin, ListAPIView):
    model = YearBook
    serializer_class = YearBookSerializer
    queryset = YearBook.objects.all().order_by('-reader_count', '-book_id')

    def get_queryset(self):
        queryset = super(BooksYearTopList, self).get_queryset()
        return queryset.filter(year=self.kwargs['year'])[:self.kwargs['top']]

    @classmethod
    def export_format_func(cls, data):
        return '\n'.join(
            '《{0[book][name]}》,{0[reader_count]}'.format(x) for x in data
        )
