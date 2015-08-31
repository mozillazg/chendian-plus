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


class OnlyFieldsModelViewMixin(object):
    only_fields_param = '_fields'

    def get_queryset(self):
        fields = self.request.query_params.get(
            self.only_fields_param, ''
        ).split(',')
        self.only_fields = only_fields = filter(None, fields)

        return super(OnlyFieldsModelViewMixin, self
                     ).get_queryset().only(*only_fields)


class ExcludeFieldsModelViewMixin(object):
    exclude_fields_param = '_exclude'

    def get_queryset(self):
        fields = self.request.query_params.get(
            self.exclude_fields_param, ''
        ).split(',')
        self.exclude_fields = exclude_fields = filter(None, fields)

        return super(ExcludeFieldsModelViewMixin, self
                     ).get_queryset().defer(*exclude_fields)


class ExcludeAndOnlySerializerMixin(object):

    @property
    def _readable_fields(self):
        fields = []
        view = self.context['view']
        if not all([hasattr(view, 'only_fields'),
                    hasattr(view, 'exclude_fields')]):
            return super(ExcludeAndOnlySerializerMixin, self)._readable_fields

        field_names = [field for field in self.fields]
        if view.only_fields:
            field_names = view.only_fields
        elif view.exclude_fields:
            field_names = set(field_names) - set(view.exclude_fields)

        for field in self.fields.values():
            if field.field_name not in field_names:
                continue

            if not field.write_only:
                fields.append(field)

        return fields
