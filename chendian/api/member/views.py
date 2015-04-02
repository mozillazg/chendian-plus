#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from django.http import Http404

from rest_framework import serializers, status, filters
from rest_framework.response import Response

from member.models import Member, NewMember
from .._base import BaseListAPIView as ListAPIView, BaseAPIView as APIView


class MemberSerializer(serializers.ModelSerializer):

    class Meta:
        model = Member
        fields = ('id', 'sn', 'qq', 'nick_name', 'description',
                  'created_at', 'updated_at')
        read_only_fields = ('id', 'created_at', 'updated_at')
        extra_kwargs = {
            'description': {'required': False},
        }


class MemberList(ListAPIView):

    model = Member
    serializer_class = Member
    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = ('sn', 'nick_name', 'qq')

    def get_queryset(self):
        kwargs = {}
        members = Member.sorted_objects.filter(**kwargs)
        return members

    def post(self, request, format=None):
        serializer = MemberSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MemberDetail(APIView):

    def get_object(self, pk):
        try:
            return Member.objects.get(pk=pk)
        except Member.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        record = self.get_object(pk)
        serializer = MemberSerializer(record)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        record = self.get_object(pk)
        serializer = MemberSerializer(record, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        member = self.get_object(pk)
        member.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class NewMemberApprove(APIView):

    def get_object(self, pk):
        try:
            return NewMember.objects.get(pk=pk)
        except NewMember.DoesNotExist:
            raise Http404

    def put(self, request, pk, format=None):
        member = self.get_object(pk)
        member.approve()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def delete(self, request, pk, format=None):
        member = self.get_object(pk)
        member.disapprove()
        return Response(status=status.HTTP_204_NO_CONTENT)
