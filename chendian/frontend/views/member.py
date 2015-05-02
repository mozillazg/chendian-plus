#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from django.core.urlresolvers import reverse_lazy
from django.http import Http404, HttpResponseRedirect
from django.views.generic.base import TemplateView


from member.models import Member


class MemberList(TemplateView):
    template_name = 'frontend/member/index.html'


class MemberDetail(TemplateView):
    template_name = 'frontend/member/detail.html'

    def get_context_data(self, **kwargs):
        context = super(MemberDetail, self).get_context_data(**kwargs)
        context['id'] = self.kwargs['pk']
        return context


def member_sn(request, sn):
    member = Member.objects.filter(sn=sn).first()
    if member is None:
        raise Http404()
    return HttpResponseRedirect(
        reverse_lazy('frontend:member_detail', kwargs={'pk': member.pk})
    )
