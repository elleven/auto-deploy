# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# from django.shortcuts import render
from rest_framework.views import APIView
from django.http import JsonResponse
from models import Department, User, UserToken
from django.utils.translation import ugettext_lazy as _
# from django.core import serializers
from rest_framework import serializers
from django.forms.models import model_to_dict
from django.utils import timezone
from rest_framework import exceptions
from rest_framework.authentication import BaseAuthentication
from utils.authentications import Zhe800Ldap
from utils.common import md5


class LdapAuth(BaseAuthentication):
    """ldap auth
    """
    def authenticate(self, request):
        token = request.data.get('token') or request.query_params.get('token')
        if not token:
            raise exceptions.AuthenticationFailed(_('auth failed'))
        token_obj = UserToken.objects.filter(token=token).first()
            # token expired check(to be build)
        if not token_obj:
            raise exceptions.AuthenticationFailed(_('auth failed'))
        return (token_obj.user, token_obj)

    def authenticate_header(self, request):
        pass


class AuthView(APIView):
    """
    login api
    """
    def post(self, request, *args, **kwargs):
        ret = {
            'code': 2001,
            'msg': u'success',
            'token': None
        }
        username = request.data.get('username', None)
        password = request.data.get('password', None)
        if not username or not password:
            ret['code'] = 5001
            ret['msg'] = _('invalid username or password')
            return JsonResponse(ret)
        try:
            ldap_obj = Zhe800Ldap(username, password)
            ldap_obj.valid
            department = ldap_obj.user['department']
            user_mail = ldap_obj.user['mail']
            department_obj, success = Department.objects.get_or_create(name=department)
            user_obj, success = User.objects.update_or_create(
                username=username, defaults={'email': user_mail, 'department_id': department_obj})
            token = md5(username)
            UserToken.objects.update_or_create(user=user_obj, defaults={'token': token})
        except Exception as why:
            ret['code'] = 5001
            ret['msg'] = str(why)
            return JsonResponse(ret)
        ret['token'] = token
        return JsonResponse(ret)


class DepartmentView(APIView):
    """
    部门api
    """
    authentication_classes = [LdapAuth, ]
    # parser_classes = [JSONParser, FormParser, ]

    def get(self, request, *args, **kwargs):
        limits = request.query_params.get('limits', 3)
        ret = {
            'code': 2000,
            'msg': u'success',
            'data': None,
               }
        try:
            datas = Department.objects.all()[:limits]
            ret['data'] = [ model_to_dict(data) for data in datas ]
        except exceptions.APIException as why:
            ret['code'] = 5000
            ret['msg'] = str(why)
        return JsonResponse(ret)

    def post(self, request, *args, **kwargs):
        ret = {
            'code': 2001,
            'msg': u'success',
            'data': None,
        }
        try:
            department_name = request.data.get('department_name')
            tel = request.data.get('tel', None)
            desc = request.data.get('desc', _('this human is too lazy to write it '))
            data, success = Department.objects.get_or_create(name=department_name, tel=tel, desc=desc)
            if not success:
                ret['code'] = 5001
                ret['msg'] = 'already exists'
            ret['data'] = model_to_dict(data)
        except exceptions.APIException as why:
            ret['code'] = 5001
            ret['msg'] = str(why)
        return JsonResponse(ret)

    def put(self, request, *args, **kwargs):
        ret = {
            'code': 2002,
            'msg': u'success',
            'data': None,
        }
        try:
            department_id = request.data.get('id', None)
            department_name = request.data.get('department_name')
            tel = request.data.get('tel')
            desc = request.data.get('desc', _('this human is too lazy to write it '))
            Department.objects.filter(id=department_id).update(name=department_name, tel=tel,
                                                               desc=desc, update_time=timezone.now())
            ret['msg'] = 'update'
        except exceptions.APIException as why:
            ret['code'] = 5002
            ret['msg'] = str(why)
        return JsonResponse(ret)

    def delete(self, request, *args, **kwargs):
        ret = {
            'code': 2003,
            'msg': u'success',
            'data': None,
        }
        try:
            department_id = request.data.get('id', None)
            Department.objects.filter(id=department_id).delete()
            ret['msg'] = 'delete'
        except exceptions.APIException as why:
            ret['code'] = 5003
            ret['msg'] = str(why)
        return JsonResponse(ret)





