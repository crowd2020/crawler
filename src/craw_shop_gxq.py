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
        #self.db = xdb.XDatabase(config.MYSQL_HOST,
        #                        config.MYSQL_DB,
        #                        config.MYSQL_PORT,
        #                        config.MYSQL_USER,
        #                        config.MYSQL_PASS)
        #self.db_handler = self.db.query2
        self.marqueen_url = "https://shop.gxq168.com/index/login"

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
        write_string += "用户 订单时间    商品    个数\n"
        today = utils.get_time_string(int(time.time()))
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
            line = user_phone + "   " + order_time + "  " + goods_name + "  " + goods_num + "\n"
            write_string += line
            self.write_file(write_string)

    def write_file(self, write_string):
        file_path = "../files/"
        file_name = utils.get_time_string(int(time.time()))
        fd = open(file_path + file_name, "w")
        fd.write(write_string)
        fd.close()


if __name__ == "__main__":
    tx = GxqShopList()
    tx.craw_marqueen()
