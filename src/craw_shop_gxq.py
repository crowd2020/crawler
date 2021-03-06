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
    def __init__(self, date):
        file_path = "../files/"
        file_name = utils.get_time_string(int(time.time()))
        self.date = date
        if self.date != "":
            file_name = self.date
        self.files = file_path + file_name + "滚雪球商城抓取结果"
        self.goods_file = file_path + "滚雪球商品列表"
        self.marqueen_url = "https://shop.gxq168.com/index/login"
        self.file_column = list()
        self.load_file()
        self.goods_dict = dict()
        self.load_goods_file()

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
        craw_day = today
        if self.date != "":
            craw_day = self.date
        uniq_list = list()
        for item in buy_list:
            idx = item.find("用户")
            if idx == -1:
                xlog.LOG.ERROR("find user error")
                continue
            user_phone = item[idx - 11:idx]
            column_list = utils.reg1(config.item_column_str, item)
            if len(column_list) < 3:
                xlog.LOG.ERROR("column_list length error")
                continue
            order_time = column_list[0]
            if order_time.find(craw_day) == -1:
                print order_time, craw_day
                xlog.LOG.ERROR("find order_time error")
                continue
            goods_num = column_list[2].split(" ")[-1]
            idx1 = item.find(config.name_str)
            idx2 = item.find("<i>x")
            goods_name = item[idx1 + len(config.name_str):idx2].strip()
            goods_price = 0
            if goods_name in self.goods_dict.keys():
                goods_price = float(self.goods_dict[goods_name])
            goods_total_price = float(goods_num) * float(goods_price)
            print user_phone, order_time, goods_name, goods_num, goods_total_price
            line = user_phone + "   " + order_time + "  " + goods_name + "  " + goods_num + "   " + str(goods_total_price)
            if line in self.file_column:
                print "column exist"
                continue
            write_string += line + "\n"
            print write_string

        if write_string != "":
            header = ""
            if len(self.file_column) == 0:
                header = "用户 订单时间    商品    个数 总积分\n"
            write_string = header + write_string
            self.write_file(write_string)

    def load_file(self):
        if os.path.exists(self.files) is False:
            return
        fd = open(self.files, "r")
        for line in fd:
            line = line.strip()
            self.file_column.append(line)

    def load_goods_file(self):
        if os.path.exists(self.goods_file) is False:
            return
        fd = open(self.goods_file, "r")
        for line in fd:
            line = line.strip()
            idx = line.rfind(" ")
            name = line[0:idx]
            price = line[idx+1:]
            self.goods_dict[name] = price

    def write_file(self, write_string):
        fd = open(self.files, "a+")
        fd.write(write_string)
        fd.close()

    def write_file(self, write_string):
        fd = open(self.files, "a+")
        fd.write(write_string)
        fd.close()


if __name__ == "__main__":
    date = ""
    if len(sys.argv) > 1:
        date = sys.argv[1]
    tx = GxqShopList(date)
    tx.craw_marqueen()
