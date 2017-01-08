#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from django.http import HttpResponse
from django.utils.decorators import classonlymethod
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
        only_fields = set(self.fields) & set(filter(None, fields))
        self.only_fields = only_fields

        return super(OnlyFieldsModelViewMixin, self
                     ).get_queryset().only(*only_fields)


class ExcludeFieldsModelViewMixin(object):
    exclude_fields_param = '_exclude'

    def get_queryset(self):
        fields = self.request.query_params.get(
            self.exclude_fields_param, ''
        ).split(',')
        exclude_fields = set(self.fields) & set(filter(None, fields))
        self.exclude_fields = exclude_fields

        return super(ExcludeFieldsModelViewMixin, self
                     ).get_queryset().defer(*exclude_fields)


class ExcludeAndOnlySerializerMixin(object):

    @property
    def _readable_fields(self):
        fields = []
        view = self.context.get('view')
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


class ExportMixin(object):
    export_param = 'export'

    @classonlymethod
    def as_view(cls, *initargs, **initkwargs):
        view = super(ExportMixin, cls).as_view(*initargs, **initkwargs)

        def _view(request, *args, **kwargs):
            response = view(request, *args, **kwargs)
            export_format = request.GET.get(cls.export_param)
            if not export_format:
                return response

            return {
                'txt': cls._export_txt,
            }.get(export_format, 'txt')(response, request.GET.get('filename'))

        return _view

    @classmethod
    def _export_txt(cls, response, filename, content_type='text/plain'):
        data = response.data
        data = cls.export_format_func(data)
        dj_response = HttpResponse(content_type=content_type)
        dj_response['Content-Disposition'] = (
            'attachment; filename="{0}"'.format(filename or 'export.txt')
        )
        dj_response.write(data)
        return dj_response

    @classmethod
    def export_format_func(cls, data):
        return unicode(data)
