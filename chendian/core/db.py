#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from django.conf import settings
from django.db import models

if settings.ENABLE_CACHING:
    from caching.base import CachingManager, CachingMixin, CachingQuerySet
else:
    CachingManager = models.Manager
    CachingMixin = type(b'CachingMixin', (object,), {})
    CachingQuerySet = models.query.QuerySet


class LogicalDeleteQuerySet(CachingQuerySet):

    def delete(self, *args, **kwargs):
        self.deleted = True
        self.save()


class ValidObjectManager(CachingManager):

    def get_queryset(self):
        return super(ValidObjectManager, self).get_queryset().exclude(
            deleted=True
        )


class LogicalDeleteMixin(CachingMixin, models.Model):
    deleted = models.BooleanField(default=False)

    raw_objects = models.Manager()
    objects = ValidObjectManager()

    class Meta:
        abstract = True

    def delete(self, _force_delete=False, *args, **kwargs):
        if _force_delete:
            return super(LogicalDeleteMixin, self).delete(*args, **kwargs)

        self.deleted = True
        self.save(*args, **kwargs)
