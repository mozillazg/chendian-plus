#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from django.db.models.aggregates import Count
from django.db.models.expressions import Value
from django.db.models.fields import IntegerField


class CountWithFunc(Count):
    """custom Count, support SQL function expression"""
    template = '%(function)s(%(distinct)s %(expression)s)'

    def __init__(self, expression, distinct=False, **extra):
        extra.update({'expression': expression})
        super(Count, self).__init__(
            'pk', distinct='DISTINCT ' if distinct else '',
            output_field=IntegerField(), **extra
        )
