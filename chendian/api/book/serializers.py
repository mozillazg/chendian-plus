#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from rest_framework import serializers
from book.models import Book


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
