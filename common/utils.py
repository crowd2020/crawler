#!/bin/env python
# -*- coding:utf-8 -*-

import re
import time

ADAY = 24*3600

def reg(r, str):
    p = re.compile(r)
    x = p.findall(str)
    if( len(x) > 0 ):
        return x[0]
    return ""

def reg1(r, str):
    p = re.compile(r)
    return p.findall(str)

def get_midnight_ts(ts):
    ts -= time.timezone
    return ts - (ts % ADAY) + time.timezone

def get_time_string(ts):
    tm = time.localtime(ts)
    return time.strftime("%Y-%m-%d %H:%M:%S", tm)
