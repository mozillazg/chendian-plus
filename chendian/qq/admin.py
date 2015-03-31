#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from django.contrib import admin
from django.core import urlresolvers
from django.utils.html import format_html

from .models import RawMessage, CheckinRecord, UploadRecord


class RawMessageAdmin(admin.ModelAdmin):
    list_display = ('sn', 'nick_name', 'qq', 'posted_at')
    list_filter = ('posted_at',)
    search_fields = ('nick_name', 'qq')
admin.site.register(RawMessage, RawMessageAdmin)


def view_raw_msg(obj):
    pk = obj.raw_msg_id
    url = urlresolvers.reverse('admin:qq_rawmessage_change', args=(pk,))
    return format_html('<a href="{0}?id={1}">{2}</a>',
                       url, pk, pk)
view_raw_msg.short_description = '原始消息记录'


class CheckinRecordAdmin(admin.ModelAdmin):
    list_display = ('pk', view_raw_msg, 'sn', 'nick_name', 'qq',
                    'book_name', 'posted_at', 'deleted')
    raw_id_fields = ('raw_msg',)
    list_filter = ('posted_at', 'deleted')
    search_fields = ('nick_name', 'qq', 'book_name')
admin.site.register(CheckinRecord, CheckinRecordAdmin)


class UploadRecordAdmin(admin.ModelAdmin):
    list_display = ('pk', 'count', 'status', 'created_at', 'update_at')
    list_filter = ('created_at', 'update_at')
admin.site.register(UploadRecord, UploadRecordAdmin)
