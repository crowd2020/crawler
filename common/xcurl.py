#!/bin/env python
#-*- coding: UTF-8 -*-

import sys
import pycurl
import StringIO


def xcurl(url, **kwargs):
    b = StringIO.StringIO()
    c = pycurl.Curl()
    c.setopt(pycurl.URL, url)
    if "proxy" in kwargs:
        c.setopt(pycurl.PROXY, kwargs["proxy"])
    c.setopt(pycurl.FOLLOWLOCATION, 1)
    if "host" in kwargs:
        c.setopt(pycurl.HTTPHEADER, ["Host: %s" % (kwargs["host"])])
    if "agent" in kwargs:
        c.setopt(pycurl.USERAGENT, kwargs["agent"])
    if "cookie" in kwargs:
        c.setopt(pycurl.COOKIE, kwargs["cookie"])
    if "referer" in kwargs:
        c.setopt(pycurl.REFERER, kwargs["referer"])
    if "postdata" in kwargs:
        c.setopt(pycurl.POSTFIELDS, kwargs["postdata"])
    c.setopt(pycurl.TIMEOUT_MS, 10000)
    c.setopt(pycurl.WRITEFUNCTION, b.write)
    try:
        c.perform()
        status = c.getinfo(pycurl.HTTP_CODE)
        if status == 200:
            resp = b.getvalue()
            return resp
        else:
            return ""
    except Exception as e:
        print e
        return ""

if __name__ == "__main__":
    url = sys.argv[1]
    print xcurl(url, postdata='{a=b}')
