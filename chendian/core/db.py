#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from django.db import models


class LogicalDeleteQuerySet(models.query.QuerySet):

    def delete(self, *args, **kwargs):
        self.deleted = True
        self.save()


class ValidObjectManager(models.Manager):

    def get_queryset(self):
        return super(ValidObjectManager, self).get_queryset().exclude(
            deleted=True
        )


class LogicalDeleteMixin(models.Model):

    deleted = models.BooleanField(default=False)

    raw_objects = models.Manager()
    objects = ValidObjectManager()

    class Meta:
        abstract = True

    def delete(self, _force_delete=False, *args, **kwargs):
        if _force_delete:
            return self.delete(*args, **kwargs)

        self.deleted = True
        self.save(*args, **kwargs)
