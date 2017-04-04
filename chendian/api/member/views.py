#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals
import datetime

from django.http import Http404
from django.shortcuts import get_object_or_404

from rest_framework import status, filters
from rest_framework.generics import (
    RetrieveUpdateDestroyAPIView
)
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

from api._base import (
    OnlyFieldsModelViewMixin, ExcludeFieldsModelViewMixin,
    BaseListAPIView as ListAPIView, BaseAPIView as APIView,
    ExportMixin
)
from api.book.serializers import BookSerializer
from api.qq.serializers import CheckinSerializer
from book.models import Book
from member.models import (
    Member, NewMember, CheckinCount, MemberYearBook, MemberYearBookCount
)
from qq.models import CheckinRecord
from .serializers import (
    MemberSerializer, DynamicMemberSerializerClass,
    CheckinCountSerializer, YearBookCountSerializer
)
from .utils import fill_calendar_for_count


class MemberList(DynamicMemberSerializerClass,
                 ExcludeFieldsModelViewMixin,
                 OnlyFieldsModelViewMixin,
                 ListAPIView):
    model = Member
    queryset = Member.objects.all()
    serializer_class = MemberSerializer
    fields = [x.field_name for x in serializer_class()._readable_fields]
    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = ('sn', 'nick_name', 'qq')

    def post(self, request, format=None):
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MemberDetail(DynamicMemberSerializerClass,
                   RetrieveUpdateDestroyAPIView):
    model = Member
    queryset = Member.objects.all()
    serializer_class = MemberSerializer


class NewMemberApprove(APIView):
    permission_classes = (IsAdminUser,)

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


class CheckinList(ListAPIView):
    model = CheckinRecord
    queryset = CheckinRecord.sorted_objects.all()
    serializer_class = CheckinSerializer

    def get_queryset(self):
        member = get_object_or_404(Member.objects.only('qq'),
                                   pk=self.kwargs['pk'])
        queryset = super(CheckinList, self).get_queryset()
        return queryset.filter(qq=member.qq).defer('raw_msg')


class BookList(ExcludeFieldsModelViewMixin,
               OnlyFieldsModelViewMixin,
               ListAPIView):
    model = Book
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    fields = [x.field_name for x in serializer_class()._readable_fields]

    def get_queryset(self):
        member = get_object_or_404(Member.objects.only('id'),
                                   pk=self.kwargs['pk'])
        queryset = super(BookList, self).get_queryset()
        return queryset.filter(readers=member)


class CheckinCountsView(APIView):
    def get(self, request, pk, year=0):
        year = int(year)
        if year < 2000:
            year = datetime.datetime.now().year
        queryset = CheckinCount.objects.filter(
            member__id=pk, checkined_at__year=year
        )
        data = CheckinCountSerializer(queryset, many=True).data
        fill_calendar_for_count(year, data)
        return Response(data)


class YearBookList(ExportMixin,
                   ListAPIView):
    model = MemberYearBook
    queryset = MemberYearBook.objects.all()
    serializer_class = BookSerializer

    @classmethod
    def export_format_func(cls, data):
        return '\n'.join('《{0[name]}》'.format(x) for x in data)

    def get_queryset(self):
        member = get_object_or_404(Member.objects.only('id'),
                                   pk=self.kwargs['pk'])
        queryset = super(YearBookList, self).get_queryset()
        return queryset.filter(member=member, year=self.kwargs['year'])

    def get_serializer(self, instance=None, *args, **kwargs):
        instance = (obj.book for obj in instance)
        return super(YearBookList, self).get_serializer(
            instance=instance, *args, **kwargs
        )


class YearBookCount(APIView):

    def get(self, request, pk, year, format=None):
        member = get_object_or_404(Member.objects.only('id'), pk=pk)
        queryset = MemberYearBookCount.objects.filter(
            member=member, year=year
        )
        serializer = YearBookCountSerializer(instance=queryset.first())
        return Response(data=serializer.data)
