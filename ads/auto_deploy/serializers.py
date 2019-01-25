# -*- coding: utf-8 -*-
from rest_framework import serializers
from models import Department, User, Service, ServiceActions, ServiceSnapshot, ServiceHosts, ActionsScripts
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
        fields = ('id', 'username', 'tel', 'email', 'department')
        depth = 1


class ServiceSerializer(serializers.ModelSerializer):

    """ 服务元数据相关字段，读写分离；
        其实建议嵌套字段关联 由view部分实现，比较好；
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


class ServiceActionsSerializer(serializers.ModelSerializer):
    """用于actions的修改，创建"""
    class Meta:
        model = ServiceActions
        fields = '__all__'
        depth = 1


class ActionsScriptsSerializer(serializers.Serializer):
    """继承Serializer，灵活度较高；
       脚本内容存储到本地,逻辑由view部分实现；
       保存脚本元数据至数据库；
        """
    id = serializers.IntegerField()
    script_name = serializers.CharField(required=True, max_length=25)
    script_languages = serializers.ChoiceField(required=True,
                                               choices=ActionsScripts.SCRIPT_LANGUAGES)
    script_content = serializers.CharField(max_length=1024, write_only=True)
    desc = serializers.CharField(max_length=255, allow_blank=True, allow_null=True)
    is_template = serializers.BooleanField(default=False)
    actions_id = serializers.IntegerField(required=True, write_only=True
                                          )

    def create(self, validated_data):
        validated_data.pop('actions_id')
        validated_data.pop('script_content')
        return ActionsScripts.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.script_name = validated_data.get('script_name', instance.script_name)
        instance.script_languages = validated_data.get('script_languages', instance.script_languages)
        instance.desc = validated_data.get('desc', instance.desc)
        instance.is_template = validated_data.get('is_template', instance.is_template)
        instance.save()
        return instance




