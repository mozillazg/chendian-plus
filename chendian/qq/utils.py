#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

import logging
import re
import sys
import traceback

from django.conf import settings
from django.utils.timezone import now
from django_rq import job
from pyquery import PyQuery

from blog.models import Tag
from core.utils import (
    str_to_utc, default_datetime_start, default_datetime_end
)
from member.models import NewMember, Member
from qq.models import RawMessage, CheckinRecord, UploadRecord
from book.models import Book, HundredGoalNote

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
                'raw_item': raw_item.strip(),
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

    d = RawMessage.raw_objects.filter(
        qq=qq, posted_at=posted_at
    )
    if d.exists():
        raw_msg = d[0]
    else:
        raw_msg = RawMessage()
        raw_msg.raw_item = raw_item
        raw_msg.nick_name = nick_name
        raw_msg.qq = qq
        raw_msg.sn = sn or None
        raw_msg.msg = msg
        raw_msg.posted_at = posted_at
        raw_msg.save()

    if callbacks:
        for callback in callbacks:
            callback(raw_msg)

    return raw_msg


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
    think = m.group('think').strip()
    posted_at = raw_msg.posted_at

    records = CheckinRecord.raw_objects.filter(
        qq=qq, posted_at=posted_at
    )
    if records.exists():
        record = records[0]
    else:
        record = CheckinRecord()
        record.raw_msg = raw_msg
        record.nick_name = nick_name
        record.qq = qq
        record.sn = sn or None
        record.book_name = book_name
        record.think = think
        record.posted_at = posted_at
        record.save()

    return record


def save_new_member(checkin_item):
    qq = checkin_item.qq
    sn = checkin_item.sn
    nick_name = checkin_item.nick_name
    posted_at = checkin_item.posted_at
    if not (sn and qq):
        return

    member = NewMember.raw_objects.filter(qq=qq)
    if not member.exists():
        member = NewMember()
        member.sn = sn
        member.qq = qq
        member.nick_name = nick_name
        member.status = NewMember.status_need
        member.last_read_at = posted_at
        member.save()
    else:
        member = member[0]
        if member.status not in [x[0] for x in NewMember.status_choices]:
            member.status = NewMember.status_need
        member.last_read_at = posted_at
        member.save()

    return member


def save_new_book(checkin_item):
    book_name = checkin_item.book_name
    posted_at = checkin_item.posted_at
    if not book_name:
        return

    book = Book.raw_objects.filter(raw_name=book_name)
    if not book.exists():
        book = Book.raw_objects.create(
            name=book_name, last_read_at=posted_at, read_count=1,
            description=book_name, raw_name=book_name
        )
    else:
        book = book[0]
        book.last_read_at = posted_at
        book.read_count += 1
        book.save()
    return book


def record_filter_kwargs(request, enable_default_range=True):
    filter_by = request.GET.get('filter_by')
    filter_value = request.GET.get('filter_value', '').strip()
    try:
        datetime_start = str_to_utc(
            request.GET.get('datetime_start', '') + ':00',
            default=default_datetime_start() if enable_default_range else None
        )
    except:
        datetime_start = None
    try:
        datetime_end = str_to_utc(
            request.GET.get('datetime_end', '') + ':00',
            default=default_datetime_end() if enable_default_range else None
        )
    except:
        datetime_end = None
    kwargs = {}
    if filter_value:
        if filter_by in ['sn', 'id']:
            if filter_value.isdigit():
                kwargs[filter_by] = filter_value
        elif filter_by == 'nick_name':
            kwargs['nick_name__contains'] = filter_value
        elif filter_by == 'book_name':
            kwargs['book_name__contains'] = filter_value
        elif filter_by in ['qq']:
            kwargs[filter_by] = filter_value
    if datetime_start:
        kwargs['posted_at__gte'] = datetime_start
    if datetime_end:
        kwargs['posted_at__lte'] = datetime_end

    return kwargs


@job
def save_uploaded_text(pk):
    r = UploadRecord.raw_objects.get(pk=pk)

    try:
        p = Parser(r.text)
        msg_list = []
        for item in p():
            raw_item = save_to_raw_db(item)
            check_in = save_to_checkin_db(raw_item)
            # TODO 改为使用信号的方式
            if check_in:
                save_new_member(check_in)
                save_new_book(check_in)
            msg_list.append(raw_item)

        r.count = len(msg_list)
        r.status = UploadRecord.status_finish
    except Exception as e:
        logger.exception(e)
        exec_info = sys.exc_info()
        r.error = u'\n'.join(traceback.format_exception(*exec_info))
        r.status = UploadRecord.status_error
    r.update_at = now()
    r.error = ''
    r.save()

    for m in Member.objects.all():
        update_member_info.delay(m.pk)
        update_member_books.delay(m.pk)


@job
def update_member_info(m_pk):
    m = Member.raw_objects.get(pk=m_pk)
    x = CheckinRecord.objects.filter(
        qq=m.qq
    ).order_by('-posted_at').first()
    if x is None:
        logger.info('member %s %s no checkin record', m.id, m.qq)
        return

    m.last_read_at = x.posted_at
    m.save()

    CheckinRecord.raw_objects.filter(qq=m.qq).update(
        sn=m.sn, nick_name=m.nick_name
    )


@job
def update_member_books(m_pk):
    member = Member.raw_objects.get(pk=m_pk)
    for c in CheckinRecord.objects.filter(qq=member.qq).values('book_name'):
        book_name = c['book_name']
        if book_name not in member.books.values('name'):
            b = Book.objects.filter(name=book_name).first()
            if b is not None:
                member.books.add(b)


def br2newline(html):
    return re.sub(r'\s*<br\s*/?>', '\n', html)


class ParseHundredGoalNote(object):

    def __init__(self, html):
        self.html = html
        self.pq = PyQuery(html)
        self.items = []

    def parse(self):
        for item in self.pq('#comments .comment-item .reply-doc'):
            result = self._parse_item(item)
            if result:
                self.items.append(result)

    def _parse_item(self, item):
        """解析单个评论"""
        pq_content = self.pq(item)
        # 忽略回复别人评论的评论
        if pq_content('.reply-quote'):
            return

        note = pq_content('p').html()
        book_name = self._parse_book_name(note)
        if not book_name:
            return

        pq_author = pq_content('h4')
        pubtime = pq_author('.pubtime').text()

        return {
            'book_name': book_name,
            'author_name': pq_author('a').text(),
            'author_url': pq_author('a').attr('href'),
            'note': br2newline(note),
            'created_at': str_to_utc(pubtime),
        }

    def _parse_book_name(self, html):
        """从笔记中解析出书名"""
        result = re.findall(ur'《([^》]+)》', html)
        if result:
            return result[0]

    def save(self):
        """将解析的所有数据保存到数据库"""
        for item in self.items:
            self._save_item(item)

    def _save_item(self, item):
        """将解析的单条数据保存到数据库"""
        if HundredGoalNote.objects.filter(
            created_at=item['created_at'], author_name=item['author_name']
        ).exists():
            return

        checkin_item = type(b'Item', (object,),
                            {'book_name': item['book_name'],
                             'posted_at': item['created_at']}
                            )
        book = save_new_book(checkin_item)
        if not book:
            return
        self._set_book_tag(book)

        obj = HundredGoalNote(**item)
        obj.book = book
        obj.save()

    def _set_book_tag(self, book, tag_name=u'百日斩'):
        """给看的书加上百日斩 tag"""
        tag, _ = Tag.objects.get_or_create(name=tag_name)
        if not book.tags.filter(pk=tag.pk).exists():
            book.tags.add(tag)

    def __call__(self):
        self.parse()
        self.save()


@job
def import_hundred_goal_note(pk):
    """百日斩"""
    r = UploadRecord.raw_objects.get(pk=pk)
    html = r.text
    try:
        parser = ParseHundredGoalNote(html)
        parser()
        r.count = len(parser.items)
        r.status = UploadRecord.status_finish
    except Exception as e:
        logger.exception(e)
        exec_info = sys.exc_info()
        r.error = u'\n'.join(traceback.format_exception(*exec_info))
        r.status = UploadRecord.status_error
    else:
        r.update_at = now()
        r.error = ''
        r.save()
