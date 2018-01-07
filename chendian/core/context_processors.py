# -*- coding: utf-8 -*-
import datetime


def past_years(request):
    now_year = datetime.datetime.now().year
    start_year = 2014
    past_years = []
    for x in range(1, 100, 1):
        year = now_year - x
        if year < start_year:
            break
        else:
            past_years.append(year)
    return {
        'past_years': past_years,
    }


def last_year(request):
    return {
        'last_year': datetime.datetime.now().year - 1,
    }
