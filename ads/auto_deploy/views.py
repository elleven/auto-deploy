# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet
from django.http import JsonResponse
from models import Department, User, UserToken, Service
from django.utils.translation import ugettext_lazy as _
# from django.core import serializers
from serializers import DepartmentSerializer, UserSerializer, ServiceSerializer
from rest_framework import exceptions
from utils.authentications import Zhe800Ldap
from utils.common import md5


class AuthView(APIView):
    """
    login api
    """
    authentication_classes = []

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
                username=username, defaults={'email': user_mail, 'department': department_obj})
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
    继承功能较少的APIView;待改进为ModelViewSet
    """
    # authentication_classes = [LdapAuth, ]
    # parser_classes = [JSONParser, FormParser, ]

    def get(self, request, *args, **kwargs):
        limits = request.query_params.get('limits', 3)
        ret = {
            'code': 2000,
            'msg': u'success',
            'data': None,
               }
        try:
            data = Department.objects.all()[:limits]
            ser = DepartmentSerializer(instance=data, many=True)
            ret['data'] = ser.data
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
            ser = DepartmentSerializer(data=request.data)
            if ser.is_valid():
                ser.save()
            else:
                ret['code'] = 5001
                ret['msg'] = ser.errors
            ret['data'] = ser.validated_data
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
            pk = request.data.get('pk', None)
            obj = Department.objects.get(pk=pk)
            ser = DepartmentSerializer(instance=obj, data=request.data)
            if ser.is_valid():
                ser.save()
            else:
                ret['code'] = 5002
                ret['msg'] = ser.errors
            ret['data'] = ser.validated_data
        except exceptions.APIException as why:
            ret['code'] = 5002
            ret['msg'] = str(why)
        except Department.DoesNotExist as why:
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
            pk = request.data.get('pk')
            Department.objects.filter(pk=pk).delete()
        except exceptions.APIException as why:
            ret['code'] = 5003
            ret['msg'] = str(why)
        return JsonResponse(ret)


class UserView(ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    # pagination_class =
    # permission_classes = ()


class ServiceView(ModelViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer


