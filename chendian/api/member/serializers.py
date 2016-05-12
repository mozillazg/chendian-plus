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
        fields = ('id', 'sn', 'nick_name', 'avatar', 'description',
                  'created_at', 'updated_at')
        read_only_fields = ('id', 'created_at', 'updated_at')
        extra_kwargs = {
            'description': {'required': False, 'trim_whitespace': False},
            'avatar': {'required': False, 'default': Member.DEFAULT_AVATAR},
        }


class MemberSerializerStaffOnly(MemberSerializer):

    class Meta(MemberSerializer.Meta):
        fields = ('id', 'sn', 'qq', 'nick_name', 'avatar', 'description',
                  'created_at', 'updated_at')


class DynamicMemberSerializerClass(object):

    def get_serializer_class(self):
        user = self.request.user
        if user.is_authenticated() and user.is_staff:
            return MemberSerializerStaffOnly
        else:
            return MemberSerializer


class CheckinCountSerializer(serializers.Serializer):
    date = serializers.DateTimeField(source='checkined_at_local',
                                     read_only=True)
    count = serializers.IntegerField()
