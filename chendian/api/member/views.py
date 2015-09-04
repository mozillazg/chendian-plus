#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from django.http import Http404
from django.shortcuts import get_object_or_404

from rest_framework import status, filters
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.response import Response

from api._base import OnlyFieldsModelViewMixin, ExcludeFieldsModelViewMixin
from api.book.serializers import BookSerializer
from api.qq.serializers import CheckinSerializer
from book.models import Book
from member.models import Member, NewMember
from qq.models import CheckinRecord
from .serializers import MemberSerializer
from api._base import BaseListAPIView as ListAPIView, BaseAPIView as APIView


class MemberList(ListAPIView):

    model = Member
    serializer_class = MemberSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = ('sn', 'nick_name', 'qq')

    def get_queryset(self):
        kwargs = {}
        members = Member.objects.filter(**kwargs)
        return members

    def post(self, request, format=None):
        serializer = MemberSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MemberDetail(RetrieveUpdateDestroyAPIView):
    model = Member
    queryset = Member.objects.all()
    serializer_class = MemberSerializer


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


class CheckinList(ListAPIView):
    model = CheckinRecord
    queryset = CheckinRecord.sorted_objects.all()
    serializer_class = CheckinSerializer

    def get_queryset(self):
        queryset = super(CheckinList, self).get_queryset()
        member = Member.objects.filter(id=self.kwargs['pk']).first()
        if member is None:
            raise Http404
        return queryset.filter(qq=member.qq)


class BookList(ExcludeFieldsModelViewMixin,
               OnlyFieldsModelViewMixin,
               ListAPIView):
    model = Book
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    fields = [x.field_name for x in serializer_class()._readable_fields]

    def get_queryset(self):
        member = get_object_or_404(Member.objects, pk=self.kwargs['pk'])
        queryset = super(BookList, self).get_queryset()
        return queryset.filter(readers=member)
