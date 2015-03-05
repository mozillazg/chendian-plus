#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

import logging
import re

from django.conf import settings

from core.utils import str_to_utc
from qq.models import RawMessage, CheckinRecord

logger = logging.getLogger(__name__)


class Parser(object):
    def __init__(self, text, msg_handlers=None):
        self.text = text.replace('\r\n', '\n')
        self.r_msg = re.compile(r"""
            (?<=\n)
            (?P<date>\d{4}\-\d{1,2}\-\d{1,2}\s+\d{1,2}:\d{1,2}:\d{1,3})  # date
            \s+
            (?P<nick_name>.*?)                                   # nick_name
            (?:\((?P<qq>\d+)\)|<(?P<email>[^>]+)>)\n             # QQ number
            (?P<msg>.*?)                                         # message
            (?=(?:\d{4}-\d{1,2}-\d{1,2})|\n+$)
        """, re.I | re.X | re.S | re.U)
        self.msg_handlers = []
        if msg_handlers:
            self.msg_handlers.extend(msg_handlers)

    def parse(self):
        for m in self.r_msg.finditer(self.text):
            raw_item = m.group(0)
            date_str = m.group('date')
            nick_name = m.group('nick_name')
            qq = m.group('qq')
            email = m.group('email')
            msg = m.group('msg')
            qq = qq or email
            yield {
                'raw_item': raw_item,
                'nick_name': re.sub(r'【\d+】', '', nick_name, re.U).strip(),
                'qq': qq.strip(),
                'sn': self._find_sn(nick_name),
                'msg': msg.strip(),
                'posted_at': str_to_utc(date_str),
            }

    def _find_sn(self, nick_name):
        m = re.findall(r'(?<=【)\d+(?=】)', nick_name, re.U)
        if m:
            return int(m[0])

    def __call__(self):
        for msg in self.parse():
            yield msg


def save_to_raw_db(msg_dict, callbacks=None):
    raw_item = msg_dict['raw_item']
    nick_name = msg_dict['nick_name']
    qq = msg_dict['qq']
    sn = msg_dict['sn']
    msg = msg_dict['msg']
    posted_at = msg_dict['posted_at']

    d = RawMessage.objects.filter(
        nick_name=nick_name, qq=qq, posted_at=posted_at
    )
    if d.exists():
        raw_msg = d[0]
    else:
        raw_msg = RawMessage()
        raw_msg.raw_item = raw_item
        raw_msg.nick_name = nick_name
        raw_msg.qq = qq
        raw_msg.sn = sn
        raw_msg.msg = msg
        raw_msg.posted_at = posted_at
        raw_msg.save()

    if callbacks:
        for callback in callbacks:
            callback(raw_msg)


def save_to_checkin_db(raw_msg, regex=settings.CHECKIN_RE):
    nick_name = raw_msg.nick_name
    qq = raw_msg.qq
    sn = raw_msg.sn
    msg = raw_msg.msg
    m = regex.match(msg)
    if not m:
        return

    # keyword = m.group('keyword')
    book_name = m.group('book_name').strip('《》')
    think = m.group('think')
    posted_at = raw_msg.posted_at

    records = CheckinRecord.objects.filter(
        nick_name=nick_name, qq=qq, posted_at=posted_at
    )
    if records.exists():
        record = records[0]
        if record.raw_msg == raw_msg:
            return
    else:
        record = CheckinRecord()
        record.raw_msg = raw_msg
        record.nick_name = nick_name
        record.qq = qq
        record.sn = sn
        record.book_name = book_name
        record.think = think
        record.posted_at = posted_at
        record.save()
