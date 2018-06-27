# -*- coding: utf-8 -*-
import ldap  # pip install python-ldap
from rest_framework import exceptions
from django.conf import settings


class Zhe800Ldap(object):
    """
    auth proxy of inner ldap
    """
    _LDAP_URL = getattr(settings,
                        'LDAP_URL', None)
    _LDAP_ROOT_DN = getattr(settings,
                            'LDAP_ROOT_DN', None)
    _LDAP_ROOT_USER = getattr(settings,
                              'LDAP_ROOT_USER', None)
    _LDAP_ROOT_PASSWORD = getattr(settings,
                                  'LDAP_ROOT_PASSWORD', None)

    def __init__(self, username, password, **kwargs):
        self.baseDN = kwargs.get('baseDN', Zhe800Ldap._LDAP_ROOT_DN)
        self.host = kwargs.get('host', Zhe800Ldap._LDAP_URL)
        self.root_user = kwargs.get('root_user', Zhe800Ldap._LDAP_ROOT_USER)
        self.root_password = kwargs.get('root_password', Zhe800Ldap._LDAP_ROOT_PASSWORD)
        self.username = username
        self.password = password
        self.ldap = ldap.initialize(self.host)
        try:
            self.ldap.simple_bind_s(self.root_user, self.root_password)
        except ldap.LDAPError as e:
            raise exceptions.AuthenticationFailed(str(e))

    def user_info(self, username, retrieveAttributes=[]):
        searchScope = ldap.SCOPE_SUBTREE
        searchFilter = 'cn=' + username
        ret = self.ldap.search_s(self.baseDN, searchScope, searchFilter, retrieveAttributes)
        if len(ret) == 0:
            raise exceptions.AuthenticationFailed('%s not exist' % self.username)
        return ret

    @property
    def user(self):
        ret = {
            'displayName': None,
            'department': None,
            'mail': None,
        }
        user_infos = self.user_info(self.username)
        for key in ret:
            ret[key] = user_infos[0][1][key][0]
        return ret

    @property
    def valid(self):
        usernameDN = self.user_info(self.username, retrieveAttributes=['DN'])[0][0]
        try:
            self.ldap.simple_bind_s(usernameDN, self.password)
            return True
        except ldap.INVALID_CREDENTIALS as e:
            raise exceptions.AuthenticationFailed(str(e))

