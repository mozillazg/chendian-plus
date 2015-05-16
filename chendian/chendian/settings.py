#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

"""
Django settings for chendian project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import re

BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '-+m+-60&5+57=2q!aufcbj8c3yzt1=yjb+iu0#&2(&vo#s=2r)'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True
TEMPLATE_DIRS = (os.path.join(BASE_DIR, 'templates'),)


TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.request",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.core.context_processors.tz",
    "django.contrib.messages.context_processors.messages",
    "django.template.context_processors.debug",
)

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'rest_framework',
    "django_rq",

    'api',
    'book',
    'core',
    'member',
    'qq',
    'frontend',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'chendian.urls'

WSGI_APPLICATION = 'chendian.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'zh-hans'

# TIME_ZONE = 'UTC'
TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

# USE_L10N = True

USE_TZ = True

DATETIME_FORMAT = "Y-m-d H:i:s"
DATE_FORMAT = "Y-m-d"
TIME_FORMAT = "H:i:s"

LOGIN_URL = 'login'


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_ROOT = os.path.join(BASE_DIR, 'assets')
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)
STATIC_URL = '/static/'
# STATICFILES_FINDERS = (
#     'django.contrib.staticfiles.finders.FileSystemFinder',
#     'django.contrib.staticfiles.finders.AppDirectoriesFinder',
# )


CHECKIN_RE = re.compile(r"""
    ^[\s#]*
    (?P<keyword>打卡)\s*
    (?P<book_name>(?:《[^》]+》)|[^\s]+)\s*
    (?P<think>.*$)""", re.U | re.X | re.S | re.I)

REST_SESSION_LOGIN = False
REST_FRAMEWORK = {
    'DEFAULT_FILTER_BACKENDS': (
        'rest_framework.filters.DjangoFilterBackend',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'api.permissions.IsAdminOrReadonly',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
    ),

    'DEFAULT_PAGINATION_CLASS': 'core.pagination.LinkHeaderPagination',
    'PAGE_SIZE': 100,

    'DATETIME_FORMAT': '%Y-%m-%d %H:%M:%S',
    'DATETIME_INPUT_FORMATS': ('%Y-%m-%d %H:%M:%S',),
    'DATE_FORMAT': '%Y-%m-%d',
    'DATE_INPUT_FORMATS': ('%Y-%m-%d',),
    'TIME_FORMAT': '%H:%M:%S',
    'TIME_INPUT_FORMATS': ('%H:%M:%S',),
}


RQ_QUEUES = {
    'default': {
        'HOST': 'localhost',
        'PORT': 6379,
        'DB': 2,
        'PASSWORD': '',
        'DEFAULT_TIMEOUT': 60 * 60 * 5,
    },
}


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'null': {
            'level': 'DEBUG',
            'class': 'logging.NullHandler',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'propagate': True,
            'level': 'DEBUG',
        },
        'django.request': {
            'handlers': ['console'],
            'level': 'ERROR',
            'propagate': False,
        },
        'qq': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
        'book': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
        'member': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
        'api': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
        'core': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
    }
}

QINIU = {
    'access_key': b'',
    'secret_key': b'',
    'bucket_name': b'',
    'base_url': b'http://foobar.qiniudn.com/{filename}',
}

DEFAULT_PASSWORD = None
RQ_SHOW_ADMIN_LINK = True
