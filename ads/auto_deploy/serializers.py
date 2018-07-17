# -*- coding: utf-8 -*-
from rest_framework import serializers
from models import Department, User, UserToken
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone


class DepartmentSerializer(serializers.ModelSerializer):

    def validate_name(self, validated_value):
        if not validated_value:
            raise serializers.ValidationError("invalid name")
        return validated_value

    def validate(self, attrs):
        attrs['desc'] = attrs.get('desc', _('this human is too lazy to write it '))
        attrs['update_time'] = attrs.get('update_time', timezone.now())
        return attrs

    class Meta:
        model = Department
        fields = ('pk', 'name', 'tel', 'desc', 'update_time')
        # depth = 2




