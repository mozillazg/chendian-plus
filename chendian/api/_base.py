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
