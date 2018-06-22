# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from rest_framework.views import APIView
from django.http import JsonResponse
from models import Department
from django.utils.translation import ugettext_lazy as _
from django.core import serializers
from django.forms.models import model_to_dict


class DepartmentView(APIView):
    """
    部门api
    """
    def get(self, request, *args, **kwargs):
        limits = request._request.GET.get('limits', 3)
        ret = {
            'code': 2000,
            'msg': None,
            'data': None,
               }
        try:
            datas = Department.objects.all()[:limits]
            ret['data'] = [ model_to_dict(data) for data in datas ]
            ret['msg'] = u'success'
        except Exception as why:
            ret['code'] = 5000
            ret['msg'] = str(why)
        return JsonResponse(ret)

    def post(self, request, *args, **kwargs):
        ret = {
            'code': 2001,
            'msg': None,
            'data': None,
        }
        try:
            department_name = request._request.POST.get('department_name')
            tel = request._request.POST.get('tel', None)
            desc = request._request.POST.get('desc', _('this human is too lazy to write it '))
            data, success = Department.objects.get_or_create(name=department_name, tel=tel, desc=desc)
            if not success:
                ret['code'] = 5001
                ret['msg'] = 'already exists'
            ret['data'] = model_to_dict(data)
        except Exception as why:
            ret['code'] = 5001
            ret['msg'] = str(why)
        return JsonResponse(ret)

    def put(self, request, *args, **kwargs):
        ret = {
            'code': 2002,
            'msg': None,
            'data': None,
        }
        try:
            department_id = request.data.get('id', None)
            department_name = request.data.get('department_name')
            tel = request.data.get('tel')
            desc = request.data.get('desc', _('this human is too lazy to write it '))
            Department.objects.filter(id=department_id).update(name=department_name, tel=tel, desc=desc)
            ret['msg'] = 'update'
        except Exception as why:
            ret['code'] = 5002
            ret['msg'] = str(why)
        return JsonResponse(ret)

    def delete(self, request, *args, **kwargs):
        ret = {
            'code': 2003,
            'msg': None,
            'data': None,
        }
        try:
            department_id = request.data.get('id', None)
            Department.objects.filter(id=department_id).delete()
            ret['msg'] = 'delete'
        except Exception as why:
            ret['code'] = 5003
            ret['msg'] = str(why)
        return JsonResponse(ret)





