#!/bin/sh

cd ./crawler/src/ 
python craw_shop_gxq.py
git add *
git commit -m "update files"
git push origin master
