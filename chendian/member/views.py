#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""成员信息"""

from __future__ import absolute_import, print_function, unicode_literals

from django.contrib.auth import (
    login as dj_login, logout as dj_logout, authenticate
)
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.generic import ListView

from member.models import Member
from .forms import LoginForm

LOGIN_URL = reverse_lazy('login')


class MemberListView(ListView):
    context_object_name = 'members'
    template_name = 'member/index.html'
    paginate_by = 15

    def get_queryset(self):
        sort = self.request.GET.get('sort', 'sn')
        kwargs = {}
        filter_by = self.request.GET.get('filter_by')
        value = self.request.GET.get('filter_value')
        if filter_by in ['sn', 'qq', 'nick_name'] and value:
            if filter_by == 'nick_name':
                kwargs['nick_name__contains'] = value
            elif filter_by == 'sn':
                if value.isdigit():
                    kwargs[filter_by] = value
            else:
                kwargs[filter_by] = value

        queryset = Member.objects.filter(**kwargs)
        if sort and sort.lstrip('-') in [
            'sn', 'nick_name', 'qq'
        ]:
            queryset = queryset.order_by(sort)
        return queryset


def login(request, template_name='login.html',
          form_class=LoginForm, extra_context=None):
    """用户登录"""
    next_url = request.GET.get('next') or '/'
    form = form_class(data=request.POST or None)
    if form.is_valid():
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(username=username, password=password)
        if user is not None and user.is_active:
            dj_login(request, user)
            return HttpResponseRedirect(next_url)

    context = {
        'form': form,
    }
    if extra_context:
        context.update(context)
    return render_to_response(template_name, context,
                              context_instance=RequestContext(request))


@login_required(login_url=LOGIN_URL)
def logout(request):
    next_url = request.GET.get('next') or LOGIN_URL
    dj_logout(request)
    return HttpResponseRedirect(next_url)
