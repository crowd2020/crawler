#!/bin/env python
# -*- coding:utf-8 -*-

marqueen_content_str = "<marquee behavior=\"scoll\"\s+scrollamount=\"14\">\s+(.*?)\s+</marquee>"
marqueen_item_str = "<span>\s+(.*?)\s+</span>"
item_column_str = "<i>(.*?)</i>"
name_str = "<i>已下单</i>"

ul_str = "<ul class=\"pro-items-list clearfix\">\s+(.*?)\s+</ul>"
li_str = "<li>\s+(.*?)\s+</li>"
goods_name_str = "<p class=\"pro-name\">(.*?)</p>"
price_str = "<p class=\"pro-price-s2\">(.*?)</p>"
