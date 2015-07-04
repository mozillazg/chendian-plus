#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from django.contrib import admin

from .models import Category, Tag, Article


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'slug', 'description',
                    'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('name', 'slug', 'description', 'detail')
admin.site.register(Category, CategoryAdmin)


class TagAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'slug', 'description',
                    'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('name', 'slug', 'description', 'detail')
admin.site.register(Tag, TagAdmin)


class ArticleAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'slug', 'author', 'status',
                    'created_at', 'updated_at')
    list_filter = ('status', 'markup', 'created_at', 'updated_at')
    search_fields = ('title', 'summary', 'slug', 'content')

    def get_queryset(self, request):
        queryset = self.model.raw_objects.get_queryset()
        return queryset.defer('content')
admin.site.register(Article, ArticleAdmin)
