#!/bin/sh

cd ./src/ 
python craw_shop_gxq.py $1
cd ../
git add *
git commit -m "update files"
git push origin master
