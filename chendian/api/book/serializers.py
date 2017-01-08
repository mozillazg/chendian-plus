#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from rest_framework import serializers

from api._base import ExcludeAndOnlySerializerMixin
from api.blog.serializers import TagSerializer   # noqa
from blog.models import Tag
from book.models import Book, HundredGoalNote, YearBook
from qq.models import CheckinRecord


class BookSerializer(ExcludeAndOnlySerializerMixin,
                     serializers.ModelSerializer):
    reader_count = serializers.SerializerMethodField(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    tag_list = serializers.ListField(write_only=True, default=None)

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
                  'last_read_at', 'reader_count', 'author',
                  'tags', 'tag_list')
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

    def update(self, instance, validated_data):
        tag_list = validated_data.pop('tag_list', []) or []
        tags = []
        for name in tag_list:
            tag, _ = Tag.objects.get_or_create(name=name)
            tags.append(tag)

        super(BookSerializer, self).update(instance, validated_data)
        instance.tags = tags
        instance.save()

        return instance


class HundredGoalNoteSerializer(ExcludeAndOnlySerializerMixin,
                                serializers.ModelSerializer):
    """百日斩打卡记录"""

    class Meta:
        model = HundredGoalNote
        fields = ('id', 'author_name', 'book_name',
                  'created_at', 'book', 'member',
                  'note', 'author_url',
                  )
        read_only_fields = ('id', 'created_at', 'book', 'member')


class YearBookSerializer(serializers.ModelSerializer):
    book = BookSerializer()

    class Meta:
        model = YearBook
        fields = ('id', 'year', 'book', 'reader_count')
