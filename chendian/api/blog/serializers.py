#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from rest_framework import serializers
from api.member.serializers import MemberSerializer
from blog.models import Article, Tag, Category


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ('id', 'name', 'slug', 'description', 'detail')


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('id', 'name', 'slug', 'description', 'detail')


class ArticleSerializer(serializers.ModelSerializer):
    author = MemberSerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    categories = CategorySerializer(many=True, read_only=True)
    tag_list = serializers.ListField(write_only=True, default=None)
    category_list = serializers.ListField(write_only=True, default=None)

    class Meta:
        model = Article
        fields = (
            'id', 'sticky', 'author', 'title', 'slug', 'summary',
            'content', 'markup', 'tags', 'categories',
            'created_at', 'updated_at',
            'tag_list', 'category_list'
        )
        read_only_fields = (
            'id', 'created_at', 'updated_at',
        )
