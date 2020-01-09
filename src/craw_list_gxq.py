#!/bin/env python
# -*- coding:utf-8 -*-

import os
import sys
sys.path.append(os.path.abspath("../common"))

import re
import time
import xdb
import xlog
import xcurl
import utils
import config


class GxqGoodsList():
    def __init__(self, session):
        self.cookie = "oa_sessionid=" + session
        file_name = "../files/滚雪球商品列表"
        self.files = file_name
        self.index_url = "https://shop.gxq168.com/?p="
        self.file_column = list()
        self.load_file()

    def craw_list(self):
        for i in range(0, 1):
            page = i + 1
            url = self.index_url + str(page)
            self.craw(url)

    def craw(self, url):
        content = xcurl.xcurl(url, cookie=self.cookie).replace("\r", "").replace("\n", "")
        if content == "":
            xlog.LOG.WARN("get content error")
            return
        print content
        content = utils.reg(config.ul_str, content)
        if content == "":
            xlog.LOG.WARN("reg content error")
            return
        li_list = utils.reg1(config.li_str, content)
        print li_list

    def load_file(self):
        if os.path.exists(self.files) is False:
            return
        fd = open(self.files, "r")
        for line in fd:
            line = line.strip()
            self.file_column.append(line)

    def write_file(self, write_string):
        fd = open(self.files, "a+")
        fd.write(write_string)
        fd.close()


if __name__ == "__main__":
    session = ""
    if len(sys.argv) < 2:
        print "Usage: session"
        exit(-1)
    session = sys.argv[1]
    tx = GxqGoodsList(session)
    tx.craw_list()
