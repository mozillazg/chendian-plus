#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from django.contrib import admin
from django.core import urlresolvers
from django.utils.html import format_html

from .models import (
    Member, NewMember, CheckinCount, MemberYearBook, MemberYearBookCount
)


def view_user(obj):
    pk = obj.user_id
    url = urlresolvers.reverse('admin:auth_user_change', args=(pk,))
    return format_html('<a href="{0}?id={1}">{2}</a>',
                       url, pk, pk)
view_user.short_description = 'User'


class MemberAdmin(admin.ModelAdmin):
    list_display = ('pk', view_user, 'sn', 'nick_name', 'qq',
                    'created_at', 'updated_at', 'last_read_at', 'deleted')
    list_filter = ('created_at', 'updated_at', 'last_read_at', 'deleted')
    search_fields = ('nick_name', 'qq')
admin.site.register(Member, MemberAdmin)


class NewMemberAdmin(admin.ModelAdmin):
    list_display = ('pk', 'sn', 'nick_name', 'qq', 'status',
                    'created_at', 'updated_at')
    list_filter = ('status', 'created_at', 'updated_at', 'deleted')
    search_fields = ('nick_name', 'qq')
admin.site.register(NewMember, NewMemberAdmin)


@admin.register(CheckinCount)
class NewMemberAdmin(admin.ModelAdmin):
    list_display = ('pk', 'member', 'count', 'checkined_at')
    list_filter = ('checkined_at', 'deleted')
    raw_id_fields = ('checkins',)


@admin.register(MemberYearBook)
class MemberYearBookAdmin(admin.ModelAdmin):
    list_display = ('pk', 'year', 'member', 'book')
    list_filter = ('year', 'deleted')


@admin.register(MemberYearBookCount)
class MemberYearBookCountAdmin(admin.ModelAdmin):
    list_display = ('pk', 'year', 'member', 'count')
    list_filter = ('year', 'deleted')
