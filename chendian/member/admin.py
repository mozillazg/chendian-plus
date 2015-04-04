#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from django.contrib import admin
from django.core import urlresolvers
from django.utils.html import format_html

from .models import Member, NewMember


def view_user(obj):
    pk = obj.user_id
    url = urlresolvers.reverse('admin:auth_user_change', args=(pk,))
    return format_html('<a href="{0}?id={1}">{2}</a>',
                       url, pk, pk)
view_user.short_description = 'User'


class MemberAdmin(admin.ModelAdmin):
    list_display = ('pk', view_user, 'sn', 'nick_name', 'qq',
                    'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('nick_name', 'qq')
admin.site.register(Member, MemberAdmin)


class NewMemberAdmin(admin.ModelAdmin):
    list_display = ('pk', 'sn', 'nick_name', 'qq', 'status',
                    'created_at', 'updated_at')
    list_filter = ('status', 'created_at', 'updated_at')
    search_fields = ('nick_name', 'qq')
admin.site.register(NewMember, NewMemberAdmin)
