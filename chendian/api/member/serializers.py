#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from rest_framework import serializers

from api._base import ExcludeAndOnlySerializerMixin
from member.models import Member


class MemberSerializer(ExcludeAndOnlySerializerMixin,
                       serializers.ModelSerializer):
    qq = serializers.SerializerMethodField()

    class Meta:
        model = Member
        fields = ('id', 'sn', 'qq', 'nick_name', 'avatar', 'description',
                  'created_at', 'updated_at')
        read_only_fields = ('id', 'created_at', 'updated_at')
        extra_kwargs = {
            'description': {'required': False, 'trim_whitespace': False},
            'avatar': {'required': False, 'default': Member.DEFAULT_AVATAR},
        }

    def get_qq(self, instance):
        user = self.context['request'].user
        if not (user.is_authenticated() and user.is_staff):
            return
        return instance.qq
