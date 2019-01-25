# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.conf import settings
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet, GenericViewSet
from rest_framework.mixins import CreateModelMixin, UpdateModelMixin
from django.http import JsonResponse
from models import Department, User, UserToken, Service, ServiceActions, ActionsScripts
from django.utils.translation import ugettext_lazy as _
from serializers import DepartmentSerializer, UserSerializer, ServiceSerializer, ServiceActionsSerializer, ActionsScriptsSerializer
from rest_framework import exceptions
from utils.authentications import Zhe800Ldap
from utils.common import md5, initial_actions
import os


class WriteOnlyModelViewSet(CreateModelMixin, UpdateModelMixin, GenericViewSet):
    """write only model view set"""
    pass


class AuthView(APIView):
    """
    用于登陆认证
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


class DepartmentViewSet(ModelViewSet):
    """用户查询增加部门配置"""
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer


class UserView(ReadOnlyModelViewSet):
    """用于用户信息查询"""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    # pagination_class =
    # permission_classes = ()


class ServiceView(ModelViewSet):
    """服务元数据信息增删改查接口，
    再删除服务时候 先删除附属配置，再删除服务元数据信息"""
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer

    def perform_create(self, serializer):
        obj = serializer.save()
        # actions initial
        actions_obj = ServiceActions()
        initial_actions(obj.id, actions_obj)


class ServiceActionsView(ModelViewSet):
    """actions 相关配置修改，创建service时候会默认初始化部署步骤信息；
    'get': 'list'  会根据owner 以及 ref_id 查询所属的actions"""
    queryset = ServiceActions.objects.all()
    serializer_class = ServiceActionsSerializer

    def list(self, request, *args, **kwargs):
        owner = request.data.get('owner', 3)
        ref_id = request.data.get('ref_id')
        queryset = self.get_queryset().filter(owner=owner, ref_id=ref_id).order_by('index')
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class ActionsScriptsView(ModelViewSet):
    """需要实现对应的action 方法 get:list post:create ...
       实现嵌套字段关联操作；
       """
    queryset = ActionsScripts.objects.all()
    serializer_class = ActionsScriptsSerializer
    _base_dir = getattr(settings, 'BASE_DIR')
    _base_script_dir = getattr(settings, 'SCRIPT_DIR', _base_dir + '/scripts')

    def list(self, request, *args, **kwargs):
        """只用于模板脚本的展示
        """
        is_template = True
        queryset = self.get_queryset().filter(is_template=is_template).order_by('create_time')
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        """保存元数据至数据库；
        保存脚本内容至本地 _base_dir/scritps/script_id/script_name.sh
        区分模板非模板；
        保存完成后 关联actions"""

        script_obj = serializer.save()
        script_obj_id, name, content = script_obj.id, script_obj.script_name, serializer.validated_data['script_content']
        script_dir = self._base_script_dir + '/' + str(script_obj_id)
        try:
            if not os.exists(script_dir):
                os.makedirs(script_dir, 0755)
            fd = os.open(script_dir + '/' + name, os.O_RDWR|os.O_CREAT, 0400)
            os.write(fd, content)
            os.close(fd)
        except OSError as why:
            print why
        try:
            actions_obj = ActionsScripts.objects.get(id=serializer.validated_data['actions_id'])
            actions_obj.script_id = script_obj
            actions_obj.save()
        except Exception as why:
            print  why

    def perform_update(self, serializer):
        """ update"""
        return self.perform_create(serializer)

    def perform_destroy(self, instance):
        """delete"""
        file_path = self._base_script_dir + '/' + str(instance.id) + '/' + instance.script_name
        os.remove(file_path)
        instance.delete()

    def retrieve(self, request, *args, **kwargs):
        """read"""
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        file_path = self._base_script_dir + '/' + str(instance.id) + '/' + instance.script_name
        with open(file_path, 'r') as fd:
            script_content = fd.read()
        serializer.data['script_content'] = script_content
        return Response(serializer.data)






