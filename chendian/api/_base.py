#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from rest_framework.generics import ListAPIView
from rest_framework.mixins import (
    CreateModelMixin, ListModelMixin, RetrieveModelMixin
)
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet


class BaseAPIView(APIView):
    pass


class BaseListAPIView(ListAPIView):
    pass


class CreateListRetrieveViewSet(CreateModelMixin,
                                ListModelMixin,
                                RetrieveModelMixin,
                                GenericViewSet):
    pass


class OnlyFieldsModelMixin(object):
    only_fields_param = '_fields'

    def get_queryset(self):
        fields = self.request.query_params.get(
            self.only_fields_param, ''
        ).split(',')
        only_fields = filter(None, fields)

        return super(OnlyFieldsModelMixin, self
                     ).get_queryset().only(*only_fields)


class ExcludeFieldsModelMixin(object):
    exclude_fields_param = '_exclude'

    def get_queryset(self):
        fields = self.request.query_params.get(
            self.exclude_fields_param, ''
        ).split(',')
        exclude_fields = filter(None, fields)

        return super(ExcludeFieldsModelMixin, self
                     ).get_queryset().exclude(*exclude_fields)
