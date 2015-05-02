#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from rest_framework import serializers
from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response
from rest_framework.views import APIView

from core.storage import Qiniu


class UploadSerializer(serializers.Serializer):
    file = serializers.FileField()


class Upload(APIView):
    parser_classes = (FileUploadParser,)

    def post(self, request):
        serializer = UploadSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        file_obj = serializer.validated_data['file']

        name = file_obj.name
        url = Qiniu().upload(file_obj.read())
        if not url:
            return Response({'detail': u'文件上传失败'}, status=599)
        return Response({'filename': name, 'url': url})
