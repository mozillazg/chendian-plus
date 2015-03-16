#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals
from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic import TemplateView

urlpatterns = patterns(
    '',
    # Examples:
    # url(r'^$', 'chendian.views.home', name='home'),
    url(r'^$', TemplateView.as_view(template_name='index.html')),
    url(r'^admin123/', include('qq.urls', namespace='qq')),
    url(r'^admin123/members', include('member.urls', namespace='member')),
    url(r'^api/', include('api.urls', namespace='api')),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += patterns(
    '',
    (r'^django-rq/', include('django_rq.urls')),
)
