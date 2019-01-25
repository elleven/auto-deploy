# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.utils import timezone
from dateutil.parser import parse
from django.conf import settings


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
    department = models.ForeignKey(
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
    服务元数据信息，用于记录服务相关数据，作为服务数据中心基础。
    """
    LANGUAGES = (
        (0, 'JAVA'),
        (1, 'RUBY'),
        (2, 'PYTHON'),
        (3, 'GO'),
        (4, 'NODE'),
    )

    TYPES = (
        (0, 'TASK'),
        (1, 'HTTP'),
        (2, 'THRIFT'),
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
    service_type = models.CharField(
        _('service type'), max_length=10, choices=TYPES)
    port = models.IntegerField(
        _('service port'), null=True, blank=True)
    desc = models.CharField(
        _('service desc'), max_length=255, null=True, blank=True)
    department = models.ForeignKey(
        Department, related_name='service_department')

    users = models.ManyToManyField(User)

    lock_ts = models.DateTimeField(null=True, blank=True)

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
        _EXPIRE_TIME = getattr(settings, 'EXPIRE_TIME', 86400)
        if not self.lock_ts:
            return False
        return ((parse(str(timezone.now()))) - parse(str(self.lock_ts))).total_seconds() < _EXPIRE_TIME

    @is_lock.setter
    def is_lock(self, value):
        self.lock_ts = value

    class Meta:
        db_table = 'service'
        ordering = ['-create_time']
        get_latest_by = 'create_time'
        verbose_name = _('service')
        verbose_name_plural = _('services')
        index_together = [['name', 'loom_id'], ]


class ServiceSnapshot(models.Model):
    """
    部署任务历史快照，记录部署的host列表，
    以及部署过程及状态的快照信息；
    """
    STATUS = (
        (0, '成功'),
        (1, '放弃'),
        (2, '部署中')
    )

    version = models.IntegerField(
        _('deploy version'), unique=True)
    service = models.ForeignKey(
        Service, related_name='service_snapshot', on_delete=models.CASCADE)
    # 0 success, 1 destroy, 2 deploy
    status = models.CharField(_('deploy status'),
                              max_length=25, null=True, blank=True, choices=STATUS)

    create_time = models.DateTimeField(
        auto_now_add=True)

    def __unicode__(self):
        return self.version

    class Meta:
        db_table = 'service_snapshot'


class ServiceExtendBase(models.Model):
    """服务相关配套配置base
    分为快照和服务两类"""

    OWNER_ID = (
        (0, 'Service'),
        (1, 'ServiceSnapshot')
    )
    # 0 belong to Service, 1 belong to ServiceSnapshot
    owner = models.CharField(max_length=25, choices=OWNER_ID)

    # Service id or ServiceSnapshot id
    ref_id = models.IntegerField()

    create_time = models.DateTimeField(
        auto_now_add=True)

    update_time = models.DateTimeField(
        default=timezone.now)

    class Meta:
        abstract = True
        index_together = ['owner', 'ref_id']


class ActionsScripts(models.Model):

    """脚本相关信息表,脚本内容文件形式存储本地目录；
    """

    SCRIPT_LANGUAGES = (
        (0, 'python'),
        (1, 'shell'),
        (2, 'ruby')
    )

#   _DEFAULT_ENV = {
#       'ADS_HOST': '%s',
#       'ADS_RSYNC_PATH': '%s',
#       'ADS_MODULE_VERSION': '%s',
#       'ADS_MODULE_NAME': '%s',
#
#   } 待完善

    script_name = models.CharField(max_length=25)

    script_languages = models.CharField(max_length=10,
                                        choices=SCRIPT_LANGUAGES)
    desc = models.CharField(max_length=255, null=True, blank=True)

    is_template = models.BooleanField(default=False)

    create_time = models.DateTimeField(
        auto_now_add=True)

    update_time = models.DateTimeField(
        default=timezone.now)


class ServiceActions(ServiceExtendBase):
    """
    service 附属actions相关配置表；
    每个服务会默认初始化几个部署步骤；
    """
    DEFAULT_EXEC_USERS = (
        (0, 'root'),
        (1, 'webuser'),
        (2, 'mobileprod'),
        (3, 'tradeuser')
    )
    _EXEC_USERS = getattr(settings, 'EXEC_USERS', DEFAULT_EXEC_USERS)

    name = models.CharField(_('action name'), max_length=25)

    exec_user = models.CharField(_('exec user'),
                                 max_length=25, choices=_EXEC_USERS, null=True, blank=True)
    script_id = models.ForeignKey(ActionsScripts, related_name='actions_script')
    # 执行顺序
    index_id = models.IntegerField()

    def __unicode__(self):
        return self.name

    class Meta:
        db_table = 'service_actions'


class ServiceHosts(ServiceExtendBase):
    """
    service附属host相关配置
    """
    ENV = (
        (0, 'Test'),
        (1, 'Preview'),
        (2, 'Production')
    )

    env = models.CharField(max_length=25,
                           choices=ENV)
    hostIp = models.CharField(max_length=255)

    class Meta:
        db_table = 'service_hosts'



