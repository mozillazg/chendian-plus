#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from rest_framework import serializers

from api._base import ExcludeAndOnlySerializerMixin
from book.models import Book, HundredGoalNote
from qq.models import CheckinRecord


class BookSerializer(ExcludeAndOnlySerializerMixin,
                     serializers.ModelSerializer):
    reader_count = serializers.SerializerMethodField(read_only=True)

    def get_reader_count(self, instance):
        query_params = self.context['request'].query_params
        if 'reader_count' not in query_params.get('_extend', '').split():
            return
        return CheckinRecord.objects.filter(
            book_name=instance.name
        ).distinct('qq').count()

    class Meta:
        model = Book
        fields = ('id', 'name', 'douban_url', 'description',
                  'created_at', 'updated_at', 'cover', 'isbn',
                  'last_read_at', 'reader_count', 'author')
        read_only_fields = (
            'id', 'created_at', 'updated_at', 'last_read_at', 'reader_count'
        )
        extra_kwargs = {
            'description': {'required': False, 'trim_whitespace': False},
            'douban_url': {'required': False},
            'cover': {'required': False},
            'isbn': {'required': False},
            'author': {'required': False},
        }


class HundredGoalNoteSerializer(ExcludeAndOnlySerializerMixin,
                                serializers.ModelSerializer):

    class Meta:
        model = HundredGoalNote
        fields = ('id', 'author_name', 'book_name',
                  'created_at', 'book', 'member',
                  'note',
                  )
        read_only_fields = ('id', 'created_at', 'book', 'member')
