#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from rest_framework import serializers

from api._base import ExcludeAndOnlySerializerMixin
from member.models import Member


class MemberSerializer(ExcludeAndOnlySerializerMixin,
                       serializers.ModelSerializer):

    class Meta:
        model = Member
        fields = ('id', 'sn', 'qq', 'nick_name', 'avatar', 'description',
                  'created_at', 'updated_at')
        read_only_fields = ('id', 'created_at', 'updated_at')
        extra_kwargs = {
            'description': {'required': False, 'trim_whitespace': False},
            'avatar': {'required': False, 'default': Member.DEFAULT_AVATAR},
        }
