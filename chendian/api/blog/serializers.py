#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from collections import namedtuple

from rest_framework import serializers

from api.member.serializers import MemberSerializer
from blog.models import Article, Tag, Category
from member.models import Member


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ('id', 'name', 'slug', 'description', 'detail')
        read_only_fields = ('id', 'slug')


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('id', 'name', 'slug', 'description', 'detail')
        read_only_fields = ('id', 'slug')


class ArticleSerializer(serializers.ModelSerializer):
    author = MemberSerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    categories = CategorySerializer(many=True, read_only=True)
    tag_list = serializers.ListField(write_only=True, default=None)
    category_list = serializers.ListField(write_only=True, default=None)

    class Meta:
        model = Article
        fields = (
            'id', 'status', 'sticky', 'author', 'title', 'slug', 'summary',
            'content', 'markup', 'tags', 'categories',
            'created_at', 'updated_at',
            'tag_list', 'category_list',
        )
        read_only_fields = (
            'id', 'sticky', 'author', 'slug', 'summary', 'markup',
            'created_at', 'updated_at', 'status'
        )

    def create(self, validated_data):
        author = Member.objects.get(user=self.context['request'].user)
        data = self.tags_and_categories(validated_data)
        tags = data.tags
        categories = data.categories

        blog = Article.objects.create(
            author=author, status=Article.STATUS_PRE_APPROVE, **validated_data
        )
        blog.tags = tags
        blog.categories = categories
        blog.save()
        return blog

    def update(self, instance, validated_data):
        data = self.tags_and_categories(validated_data)
        tags = data.tags
        categories = data.categories

        super(ArticleSerializer, self).update(instance, validated_data)
        instance.tags = tags
        instance.categories = categories
        instance.save()

        return instance

    def tags_and_categories(self, validated_data):
        tag_list = validated_data.pop('tag_list', []) or []
        category_list = validated_data.pop('category_list', []) or []
        tags = []
        for name in tag_list:
            tag, _ = Tag.objects.get_or_create(name=name)
            tags.append(tag)
        categories = []
        for pk in category_list:
            category = Category.objects.filter(pk=pk).first()
            if category is not None:
                categories.append(category)

        return namedtuple('Result', ['tags', 'categories'])(tags, categories)
