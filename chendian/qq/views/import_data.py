#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

import collections
from time import time

from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponseRedirect
from django.views.generic import ListView

from blog.utils import import_lofter
from qq.models import UploadRecord
from qq.utils import save_uploaded_text, import_hundred_goal_note


def upload(request, extra_context=None):
    if request.method == 'POST':
        text = request.FILES.get('text').read().decode('utf-8-sig')
        type = request.POST.get('type', UploadRecord.type_qq)
        if type not in map(str, dict(UploadRecord.type_choices)):
            type = UploadRecord.type_qq
        else:
            type = int(type)
        r = UploadRecord.objects.create(text=text, type=int(type))
        if type == UploadRecord.type_qq:
            save_uploaded_text.delay(r.pk)
        elif type == UploadRecord.type_hundred_goal_note:
            import_hundred_goal_note.delay(r.pk)
        else:
            import_lofter.delay(r.pk)

    return HttpResponseRedirect(reverse_lazy('qq:import_list')
                                + '?%s' % time())


class UploadRecordList(ListView):
    context_object_name = 'records'
    template_name = 'qq/import.html'
    paginate_by = 30

    def get_queryset(self):
        queryset = UploadRecord.objects.all()
        queryset = queryset.defer('text').order_by('-update_at')
        return queryset

    def get_context_data(self, **kwargs):
        context = super(UploadRecordList, self).get_context_data(**kwargs)
        context['types'] = collections.OrderedDict(
            reversed(UploadRecord.type_choices)
        )
        return context
