#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from time import time

from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponseRedirect
from django.views.generic import ListView

from qq.models import UploadRecord
from qq.utils import save_uploaded_text


def upload(request, extra_context=None):
    if request.method == 'POST':
        text = request.FILES.get('text').read().decode('utf-8-sig')
        r = UploadRecord.objects.create(text=text)
        save_uploaded_text.delay(r.pk)
    return HttpResponseRedirect(reverse_lazy('qq:import_list')
                                + '?%s' % time())


class UploadRecordList(ListView):
    context_object_name = 'records'
    template_name = 'qq/import.html'
    paginate_by = 30

    def get_queryset(self):
        queryset = UploadRecord.objects.all().order_by('-update_at')
        return queryset
