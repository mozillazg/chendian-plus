#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from django.http import Http404

from rest_framework import serializers, status, filters, generics
from rest_framework.response import Response
from rest_framework.views import APIView

from qq.models import CheckinRecord
from qq.utils import record_filter_kwargs


class CheckinSerializer(serializers.ModelSerializer):
    raw_msg = serializers.CharField(source='raw_msg.raw_item', read_only=True)
    posted_at = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S',
                                          source='posted_at_local',
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


class CheckinList(generics.ListAPIView):

    model = CheckinRecord
    serializer_class = CheckinSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = ('sn', 'nick_name', 'qq', 'book_name')

    def get_queryset(self):
        kwargs = record_filter_kwargs(self.request, enable_default_range=False)
        records = CheckinRecord.sorted_objects.filter(**kwargs)
        return records


class CheckinDetail(APIView):

    def get_object(self, pk):
        try:
            return CheckinRecord.objects.get(pk=pk)
        except CheckinRecord.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        record = self.get_object(pk)
        serializer = CheckinSerializer(record)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        record = self.get_object(pk)
        serializer = CheckinSerializer(record, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        record = self.get_object(pk)
        record.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
