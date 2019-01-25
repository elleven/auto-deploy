# -*- coding: utf-8 -*-


def md5(username):
    import hashlib
    import time
    ctime = str(time.time())
    m = hashlib.md5(username)
    m.update(ctime)
    return m.hexdigest()


def initial_actions(serviceid, actions_obj, owner=0):

    default_actions = {
        0: '更新文件',
        1: '重启进程',
        2: '检查部署'
    }
    for index, actions_name in default_actions:
        actions_obj.owner = owner
        actions_obj.index = index
        actions_obj.ref_id = serviceid
        actions_obj.name = actions_name
        actions_obj.save()

