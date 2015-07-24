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

    class Media:
        # css = {
        #     'all': (
        #         'https://dn-tmp.qbox.me/bootstrap-3.3.2/css/bootstrap.min.css',
        #         'https://dn-tmp.qbox.me/summernote-0.6.9/summernote.css',
        #         'https://dn-tmp.qbox.me/font-awesome-4.3.0/css/font-awesome.min.css',
        #     ),
        # }
        # js = (
        #     'https://dn-tmp.qbox.me/chendian/libs/jquery.2.1.3.min.js',
        #     'https://dn-tmp.qbox.me/bootstrap-3.3.2/js/bootstrap.min.js',
        #     'https://dn-tmp.qbox.me/summernote-0.6.9/summernote.min.js',
        #     'https://dn-tmp.qbox.me/summernote-0.6.9/lang/summernote-zh-CN.js',
        #     'https://dn-tmp.qbox.me/chendian/admin.84234b.js',
        # )
        pass

    def get_queryset(self, request):
        queryset = self.model.raw_objects.get_queryset()
        return queryset.defer('content')
admin.site.register(Article, ArticleAdmin)
