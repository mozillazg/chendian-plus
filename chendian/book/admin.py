#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from django.contrib import admin

from .models import Book, HundredGoalNote


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'created_at', 'updated_at', 'last_read_at',)
    list_filter = ('created_at', 'updated_at', 'last_read_at', 'deleted')
    search_fields = ('name',)


@admin.register(HundredGoalNote)
class HundredGoalNoteAdmin(admin.ModelAdmin):
    list_display = ('pk', 'book_name', 'author_name', 'created_at')
    list_filter = ('created_at', 'updated_at', 'deleted')
    search_fields = ('book_name', 'author_name')
