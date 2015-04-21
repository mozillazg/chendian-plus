#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from rest_framework.authentication import SessionAuthentication
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView


class BaseAPIView(APIView):
    pass
    # authentication_classes = (SessionAuthentication,)
    # permission_classes = (IsAuthenticated,)


class BaseListAPIView(ListAPIView):
    pass
    # authentication_classes = (SessionAuthentication,)
    # permission_classes = (IsAuthenticated,)
