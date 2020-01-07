#!/bin/env python
# -*- coding:utf-8 -*-

import inspect

def last_func(msg):
    func = inspect.currentframe().f_back.f_back
    prefix = "[%s:%d] " % (func.f_code.co_name, func.f_lineno)
    ret = prefix + msg
    return ret
