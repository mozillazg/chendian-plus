# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand

from member.models import Member
from book.jobs import update_year_book, update_member_year_book
from book.models import Book


class Command(BaseCommand):
    help = 'Generate year data'

    def add_arguments(self, parser):
        parser.add_argument('year', type=int)

    def handle(self, *args, **options):
        year = options['year']
        for member in Member.objects.all().only('id'):
            update_member_year_book(member_id=member.pk, year=year)

        for book in Book.objects.all().only('id'):
            update_year_book(book_id=book.pk, year=year)

        self.stdout.write(
            self.style.MIGRATE_SUCCESS(
                'Successfully generate data for year %s' % year
            )
        )
