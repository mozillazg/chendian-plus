#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from rest_framework import serializers

from api._base import ExcludeAndOnlySerializerMixin
from qq.models import CheckinRecord


class CheckinSerializer(ExcludeAndOnlySerializerMixin,
                        serializers.ModelSerializer):
    posted_at = serializers.DateTimeField(source='posted_at_local',
                                          read_only=True)

    class Meta:
        model = CheckinRecord
        fields = ('id', 'sn', 'nick_name', 'book_name', 'think', 'posted_at')
        read_only_fields = ('id', 'posted_at')
        extra_kwargs = {
            'sn': {'required': False},
            'think': {'required': False},
        }


class CheckinSerializerStaffOnly(CheckinSerializer):
    raw_msg = serializers.CharField(source='raw_msg.raw_item',
                                    read_only=True)

    class Meta(CheckinSerializer.Meta):
        fields = ('id', 'sn', 'qq', 'nick_name', 'book_name',
                  'think', 'raw_msg', 'posted_at')
        read_only_fields = ('id', 'raw_msg', 'posted_at')


class DynamicCheckinSerializerClass(object):

    def get_serializer_class(self):
        user = self.request.user
        if user.is_authenticated() and user.is_staff:
            return CheckinSerializerStaffOnly
        else:
            return CheckinSerializer
