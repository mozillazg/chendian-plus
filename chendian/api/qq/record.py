#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from rest_framework import filters
from rest_framework.generics import RetrieveUpdateDestroyAPIView

from api._base import BaseListAPIView as ListAPIView
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


class CheckinDetail(RetrieveUpdateDestroyAPIView):
    queryset = CheckinRecord.objects.all()
    serializer_class = CheckinSerializer
