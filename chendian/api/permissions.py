#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from django.contrib.auth.models import User
from rest_framework.permissions import BasePermission, SAFE_METHODS

from member.models import Member


class IsAdminOrReadonly(BasePermission):

    def has_permission(self, request, view):
        return True

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True

        # always allow GET, HEAD or OPTIONS requests
        if request.user and request.user.is_staff:
            return True

        if isinstance(obj, User):
            return request.user == obj

        if isinstance(obj, Member):
            return request.user == obj.user

        return False
