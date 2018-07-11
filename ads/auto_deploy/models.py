# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.utils import timezone


class Department(models.Model):
    """
    用于定义部门/服务归属业务方
    """
    name = models.CharField(
        _('department name'), max_length=125, unique=True,
        db_index=True)

    tel = models.CharField(
        _('tel'), max_length=125, null=True)

    desc = models.CharField(
        _('department desc'), max_length=255, null=True)

    create_time = models.DateTimeField(
        auto_now_add=True)

    update_time = models.DateTimeField(
        default=timezone.now)

    def __unicode__(self):
        return self.name

    def __str__(self):
        return '(Department: %s, %s)' % (self.name, self.desc)

    class Meta:
        db_table = 'department'


class User(models.Model):
    """
    用户信息
    """

    username = models.CharField(
        _('user name'), max_length=125, unique=True,
        db_index=True
    )
    password = models.CharField(
        max_length=125)

    tel = models.CharField(
        _('user tel'), max_length=32, null=True
    )
    email = models.EmailField(
        _('user email')
    )
    department_id = models.ForeignKey(
        Department, related_name='user_department')

    create_time = models.DateTimeField(
        auto_now_add=True)

    update_time = models.DateTimeField(
        default=timezone.now)

    def __unicode__(self):
        return self.username

    class Meta:
        db_table = 'user'


class UserToken(models.Model):
    """
    用户token信息
    """
    user = models.OneToOneField(User)

    token = models.CharField(max_length=126)

    class Meta:
        db_table = 'user_token'


class Service(models.Model):
    """
    定义发布服务主体对象。
    """
    LANGUAGES = (
        ('java', 'JAVA'),
        ('ruby', 'RUBY'),
        ('python', 'PYTHON'),
        ('go', 'GO'),
        ('node', 'NODE'),
    )

    TYPES = (
        ('task', 'TASK'),
        ('http', 'HTTP'),
        ('thrift', 'THRIFT'),
    )

    name = models.CharField(
        _('service name'), max_length=125, db_index=True,
        unique=True)
    address = models.CharField(
        _('git address'), max_length=255)
    language = models.CharField(
        _('language'), max_length=10, choices=LANGUAGES)
    program_path = models.CharField(
        _('program_path'), max_length=125)
    loom_id = models.CharField(
        _('loom_id'), max_length=125,
        db_index=True, unique=True,
        help_text=_('id for service discovery'))
    type = models.CharField(
        _('service type'), max_length=10, choices=TYPES)
    port = models.IntegerField(
        _('service port'), null=True, blank=True)
    desc = models.CharField(
        _('service desc'), max_length=255)
    department_id = models.ForeignKey(
        Department, related_name='service_department')

    user_id = models.ManyToManyField(User)

    lock_ts = models.BooleanField(default=False)

    pre_version_count = models.IntegerField(default=0)

    test_version_count = models.IntegerField(default=0)

    pro_version_count = models.IntegerField(default=0)

    create_time = models.DateTimeField(
        auto_now_add=True)

    update_time = models.DateTimeField(
        default=timezone.now)

    def __unicode__(self):
        return self.name

    @property
    def is_lock(self):
        return self.lock_ts

    class Meta:
        db_table = 'service'
        ordering = ['-create_time']
        get_latest_by = 'create_time'
        verbose_name = _('service')
        verbose_name_plural = _('services')
        index_together = [['name', 'loom_id'],
                          ]






