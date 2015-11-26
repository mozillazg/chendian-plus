#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from django.contrib.auth.models import User
from rest_framework.permissions import SAFE_METHODS, IsAuthenticated

from blog.models import Article, Tag
from book.models import Book
from member.models import Member


class IsAdminOrReadonly(IsAuthenticated):

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        else:
            return super(IsAdminOrReadonly, self).has_permission(
                request, view
            )

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True

        # always allow GET, HEAD or OPTIONS requests
        if request.user and request.user.is_authenticated() \
                and request.user.is_staff:
            return True

        if isinstance(obj, Book):
            return request.user and request.user.is_authenticated()

        if isinstance(obj, User):
            return request.user == obj

        if isinstance(obj, Member):
            return request.user == obj.user

        return False


class IsAdminOrReadAndCreate(IsAuthenticated):

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        else:
            return super(IsAdminOrReadAndCreate, self).has_permission(
                request, view
            )

    def has_object_permission(self, request, view, obj):
        if not super(IsAdminOrReadAndCreate, self).has_object_permission(
            request, view, obj
        ):
            return False

        if request.method in SAFE_METHODS or request.user.is_staff \
                or isinstance(obj, Tag):
            return True

        if isinstance(obj, Article) and request.method != 'POST':
            return obj.author.user == request.user

        return False
