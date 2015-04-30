#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from rest_framework import serializers
from rest_framework.generics import (
    ListAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
)

from api.qq.serializers import CheckinSerializer
from book.models import Book
from qq.models import CheckinRecord


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ('id', 'name', 'douban_url', 'description',
                  'created_at', 'updated_at', 'cover', 'isbn',
                  'last_read_at', 'read_count')
        read_only_fields = (
            'id', 'created_at', 'updated_at', 'last_read_at', 'read_count'
        )
        extra_kwargs = {
            'description': {'required': False},
            'douban_url': {'required': False},
            'cover': {'required': False},
            'isbn': {'required': False},
        }


class BookList(ListCreateAPIView):
    model = Book
    queryset = Book.objects.all().order_by('-last_read_at')
    serializer_class = BookSerializer
    filter_fields = ('isbn', 'name')


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
