#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from django.http import Http404

from rest_framework import status, filters
from rest_framework.response import Response

from api._base import BaseListAPIView as ListAPIView, BaseAPIView as APIView
from qq.models import CheckinRecord
from qq.utils import record_filter_kwargs
from .serializers import CheckinSerializer


class CheckinList(ListAPIView):

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
        serializer = CheckinSerializer(record, context={'request': request})
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        record = self.get_object(pk)
        serializer = CheckinSerializer(record, data=request.data,
                                       context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        record = self.get_object(pk)
        record.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
