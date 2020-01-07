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


class GxqShopList():
    def __init__(self):
        file_path = "../files/"
        file_name = utils.get_time_string(int(time.time()))
        self.files = file_path + file_name + "滚雪球商城抓取结果"
        self.marqueen_url = "https://shop.gxq168.com/index/login"
        self.file_column = list()
        self.load_file()

    def craw_marqueen(self):
        content = xcurl.xcurl(self.marqueen_url).replace("\r", "").replace("\n", "")
        if content == "":
            xlog.LOG.WARN("get marqueen_url content error")
            return
        buy_content = utils.reg(config.marqueen_content_str, content)
        if buy_content == "":
            xlog.LOG.WARN("get marquee content error")
            return
        buy_list = utils.reg1(config.marqueen_item_str, buy_content)
        write_string = ""
        today = utils.get_time_string(int(time.time()))
        uniq_list = list()
        for item in buy_list:
            idx = item.find("用户")
            if idx == -1:
                continue
            user_phone = item[idx - 11:idx]
            column_list = utils.reg1(config.item_column_str, item)
            if len(column_list) < 3:
                continue
            order_time = column_list[0]
            if order_time.find(today) == -1:
                continue
            goods_num = column_list[2].split(" ")[-1]
            idx1 = item.find(config.name_str)
            idx2 = item.find("<i>x")
            goods_name = item[idx1 + len(config.name_str):idx2].strip()
            print user_phone, order_time, goods_name, goods_num
            line = user_phone + "   " + order_time + "  " + goods_name + "  " + goods_num
            if line in self.file_column:
                print "column exist"
                continue
            write_string += line + "\n"

        if write_string != "":
            header = ""
            if len(self.file_column) == 0:
                header = "用户 订单时间    商品    个数\n"
            write_string = header + write_string
            self.write_file(write_string)

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
    tx = GxqShopList()
    tx.craw_marqueen()
