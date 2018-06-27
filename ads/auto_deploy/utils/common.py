# -*- coding: utf-8 -*-


def md5(username):
    import hashlib
    import time
    ctime = str(time.time())
    m = hashlib.md5(username)
    m.update(ctime)
    return m.hexdigest()
