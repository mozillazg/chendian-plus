#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from rest_framework import serializers

from qq.models import CheckinRecord


class CheckinSerializer(serializers.ModelSerializer):
    raw_msg = serializers.CharField(source='raw_msg.raw_item', read_only=True)
    posted_at = serializers.DateTimeField(source='posted_at_local',
                                          read_only=True)

    class Meta:
        model = CheckinRecord
        fields = ('id', 'sn', 'qq', 'nick_name', 'book_name',
                  'think', 'raw_msg', 'posted_at')
        read_only_fields = ('id', 'raw_msg', 'posted_at')
        extra_kwargs = {
            'sn': {'required': False},
            'think': {'required': False},
        }
