#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.auth.decorators import permission_required
# from django.views.generic import TemplateView

from qq.views.index import HomeListView

login_url = 'login'
admin_prefix = settings.ADMIN_PREFIX

urlpatterns = patterns(
    '',

    # Examples:
    # url(r'^$', 'chendian.views.home', name='home'),
    url(r'^admin123/$', permission_required(
        'member.member_add', login_url=login_url
    )(HomeListView.as_view()), name='admin123'
    ),
    url(r'^admin123/', include('qq.urls', namespace='qq')),
    url(r'^admin123/members/', include('member.urls', namespace='member')),
    url(r'^admin123/books/', include('book.urls', namespace='book')),
    url(r'^admin123/blog/', include('blog.urls', namespace='blog')),
    url(r'^api/', include('api.urls', namespace='api')),
    # url(r'^blog/', include('blog.urls')),

    url(r'^%s/' % admin_prefix, include(admin.site.urls)),

    url(r'', include('frontend.urls', namespace='frontend')),
)

urlpatterns += patterns(
    '',
    url(r'^django-rq/', include('django_rq.urls')),
    url(r'^login/$', 'member.views.login', name='login'),
    url(r'^logout/$', 'member.views.logout', name='logout'),
    url(r'^change-password/$', 'member.views.change_password',
        name='change_password'),
)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += patterns(
        '',
        url(r'^__debug__/', include(debug_toolbar.urls)),
    )
