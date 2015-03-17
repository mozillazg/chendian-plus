#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from .settings import *

DEBUG = False
TEMPLATE_DEBUG = False
ALLOWED_HOSTS = ['127.0.0.1', '3sd.me', 'cd.3sd.me']


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'chendian',
        'USER': 'chendian',
        'PASSWORD': 'chendian',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}
