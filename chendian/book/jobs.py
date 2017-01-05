# -*- coding: utf-8 -*-
from django.db.models import Q
from django_rq import job

from book.models import Book, YearBook
from member.models import Member, MemberYearBook, MemberYearBookCount
from qq.models import CheckinRecord

CHECKIN_POSTED_AT_WHERE_YEAR = "extract(year from posted_at::TIMESTAMPTZ AT TIME ZONE '+08:00'::INTERVAL) = %s"   # noqa


@job
def update_member_year_book(member_id, year):
    member = Member.objects.filter(pk=member_id).only('qq').first()
    qq = member.qq
    checkins = CheckinRecord.objects.extra(where=[
        CHECKIN_POSTED_AT_WHERE_YEAR
     ], params=[year]).filter(qq=qq).distinct('book_name')

    for checkin in checkins:
        book_name = checkin.book_name
        book = Book.objects.filter(
            Q(name=book_name) | Q(raw_name=book_name)
        ).only('pk').first()
        if book is None:
            continue

        MemberYearBook.objects.get_or_create(
            year=year, member=member, book=book
        )

    update_member_year_book_count.delay(member_id, year)


@job
def update_member_year_book_count(member_id, year):
    count = MemberYearBook.objects.filter(
        year=year, member_id=member_id
    ).distinct('book_id').count()
    obj, _ = MemberYearBookCount.objects.get_or_create(
        year=year, member_id=member_id
    )
    obj.count = count
    obj.save()


@job
def update_year_book(book_id, year):
    count = MemberYearBook.objects.filter(
        year=year, book_id=book_id
    ).distinct('member_id').count()
    obj, _ = YearBook.objects.get_or_create(
        year=year, book_id=book_id
    )
    obj.reader_count = count
    obj.save()
