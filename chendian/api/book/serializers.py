#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from rest_framework import serializers
from book.models import Book
from qq.models import CheckinRecord


class BookSerializer(serializers.ModelSerializer):
    reader_count = serializers.SerializerMethodField(read_only=True)

    def get_reader_count(self, instance):
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
            'description': {'required': False},
            'douban_url': {'required': False},
            'cover': {'required': False},
            'isbn': {'required': False},
            'author': {'required': False},
        }
