#!/usr/bin/env python
# -*- coding: utf-8 -*-

bind = 'unix:/var/run/supervisord/chendian_web.sock'
pidfile = '/var/run/supervisord/chendian_web.pid'
proc_name = 'chendian_web'
workers = 1
user = 'nobody'
loglevel = 'error'
errorlog = '-'
accesslog = '-'
secure_scheme_headers = {
    'X-SCHEME': 'https',
}
x_forwarded_for_header = 'X-FORWARDED-FOR'
timeout = 120
