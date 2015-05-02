#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from django.conf import settings

import qiniu

qn_settings = settings.QINIU


class Qiniu(object):

    def __init__(self):
        self.qn = qiniu.Auth(
            qn_settings['access_key'], qn_settings['secret_key']
        )

    def upload(self, data, filename=None, params=None,
               mime_type='application/octet-stream',
               check_crc=False, *args, **kwargs):
        token = self.qn.upload_token(qn_settings['bucket_name'])

        ret, _ = qiniu.put_data(
            token, filename, data, params=params,
            mime_type=mime_type, check_crc=check_crc, *args, **kwargs
        )
        finall_name = ret and ret['key']
        if finall_name:
            return qn_settings['base_url'].format(filename=finall_name)
