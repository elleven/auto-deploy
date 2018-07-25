# -*- coding: utf-8 -*-
from rest_framework import serializers
from models import Department, User, Service
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone


class DepartmentSerializer(serializers.ModelSerializer):

    def validate_name(self, validated_value):
        # 校验命名规则
        return validated_value

    def validate(self, attrs):
        attrs['desc'] = attrs.get('desc', _('this human is too lazy to write it '))
        attrs['update_time'] = attrs.get('update_time', timezone.now())
        return attrs

    class Meta:
        model = Department
        fields = ('id', 'name', 'tel', 'desc', 'update_time')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'tel', 'email', 'department')
        depth = 1


class ServiceSerializer(serializers.ModelSerializer):

    """ 目前需求：1/获取服务信息接口时候可以嵌套查询，指定深度.
                 2/创建或更新服务配置的时候，嵌套字段只读保存即可；无须更改嵌套字段.
        解决方法：1/增加只写字段，读写字段分离，满足需求；
        """
    department_id = serializers.CharField(write_only=True)
    user_id = serializers.ListField(write_only=True)
    # language = serializers.CharField(source='get_language_display')
    # service_type = serializers.CharField(source='get_service_type_display')
    is_lock = serializers.SerializerMethodField()
    users = serializers.SerializerMethodField()

    def get_users(self, row):
        return [user.username for user in row.users.all()]

    def get_is_lock(self, row):
        return row.is_lock

    def validate_name(self, validated_value):
        # 服务命名规范
        return validated_value

    def validate_loom_id(self, validated_value):
        # loom-id 命名规范
        return validated_value

    def validate_department_id(self, validated_value):
        try:
            obj = Department.objects.get(name=validated_value)
        except Department.DoesNotExist as why:
            raise serializers.ValidationError("%s :%s" % (why, validated_value))
        return obj

    def validate_user_id(self, validated_value):
        obj_list = []
        for username in validated_value:
            try:
                obj = User.objects.get(username=username)
                obj_list.append(obj)
            except User.DoesNotExist as why:
                raise serializers.ValidationError("%s :%s" % (why, username))
        return obj_list

    def validate(self, attrs):
        attrs['desc'] = attrs.get('desc', _('this human is too lazy to write it '))
        attrs['update_time'] = attrs.get('update_time', timezone.now())
        return attrs

    def create(self, validated_data):
        user_obj_list = validated_data.pop('user_id')
        validated_data['department'] = validated_data.pop('department_id')
        obj = Service.objects.create(**validated_data)
        for user_obj in user_obj_list:
            obj.users.add(user_obj)
        return obj

    def update(self, instance, validated_data):
        user_obj_list = validated_data.pop('user_id')
        validated_data['department'] = validated_data.pop('department_id')
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        for user_obj in user_obj_list:
            instance.users.add(user_obj)
        instance.save()
        return instance

    class Meta:
        model = Service
        exclude = ('lock_ts', 'create_time', )
        depth = 1
