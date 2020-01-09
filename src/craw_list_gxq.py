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
    def __init__(self, uid, session):
        self.cookie = "oa_sessionid=" + session + ";oa_uid=" + uid
        file_name = "../files/滚雪球商品列表"
        self.files = file_name
        self.index_url = "https://shop.gxq168.com/?p="

    def craw_list(self):
        goods_string = ""
        for i in range(0, 31):
            page = i + 1
            url = self.index_url + str(page)
            lines = self.craw(url)
            goods_string = goods_string + lines

        if goods_string != "":
            self.write_file(goods_string)

    def craw(self, url):
        content = xcurl.xcurl(url, cookie=self.cookie).replace("\r", "").replace("\n", "")
        if content == "":
            xlog.LOG.WARN("get content error")
            return ""
        content = utils.reg(config.ul_str, content)
        if content == "":
            xlog.LOG.WARN("reg content error")
            return ""
        li_list = utils.reg1(config.li_str, content)
        write_string = ""
        for li_content in li_list:
            goods_name = utils.reg(config.goods_name_str, li_content)
            goods_name = re.sub(r'</?\w+[^>]*>', '', goods_name)
            price_str = utils.reg(config.price_str, li_content)
            idx = price_str.find('积分')
            price_str = price_str[0:idx].replace(",", "")
            write_string += goods_name + " " + price_str + "\n"
        return write_string

    def write_file(self, write_string):
        fd = open(self.files, "w")
        fd.write(write_string)
        fd.close()


if __name__ == "__main__":
    session = ""
    if len(sys.argv) < 3:
        print "Usage: uid session"
        exit(-1)
    session = sys.argv[1]
    uid = sys.argv[2]
    tx = GxqGoodsList(uid, session)
    tx.craw_list()
