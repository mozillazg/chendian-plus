#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from django import forms
from django.contrib.auth.forms import AuthenticationForm

class LoginForm(AuthenticationForm):
    error_messages = {
        'invalid_login': '用户名或密码错误！',
        'no_cookies': '您的浏览器没有启用 Cookies！',
        'inactive': '此账户未激活！',
    }
