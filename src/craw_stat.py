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


class GxqShopStat():
    def __init__(self):
        file_path = "../files/"
        self.file_name = utils.get_time_string(int(time.time()))
        self.files = file_path + self.file_name + "滚雪球商城抓取结果"
        self.stat_file = file_path + "滚雪球商城抓取结果汇总"

    def stat(self):
        today_total = self.load_current_file()
        print today_total
        self.rewrite_stat_file(today_total)

    def load_current_file(self):
        if os.path.exists(self.files) is False:
            print "file not exist"
            return 0
        fd = open(self.files, "r")
        row = 0
        total = 0
        for line in fd:
            if row == 0:
                row += 1
                continue
            slist = line.strip().split(" ")
            money = int(slist[-1].split(".")[0])
            total += money
        return total

    def rewrite_stat_file(self, today_total):
        if os.path.exists(self.stat_file) is False:
            return
        fd = open(self.stat_file, "r")
        line_list = list()
        for line in fd:
            line_list.append(line.strip())
        ###忽略异常
        last_line = line_list[-1]
        last_line_list = last_line.split(" ")
        date_string = last_line_list[0]
        total_money = int(line_list[-2].split(" ")[-1])
        added_total = total_money + today_total
        string = self.file_name + " " + str(today_total) + " " + str(added_total)
        today = self.file_name
        if today != date_string:
            line_list.append(string)
        else:
            line_list[-1] = string
        fd.close()
        self.write_file(line_list)

    def write_file(self, line_list):
        write_string = "\n".join(line_list)
        print write_string
        fd = open(self.stat_file, "w")
        fd.write(write_string)
        fd.close()

if __name__ == "__main__":
    tx = GxqShopStat()
    tx.stat()
