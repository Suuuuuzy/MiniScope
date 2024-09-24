#!/bin/bash
# start appium
./run_appium.sh

# record the data of miniapp id and its download dir
adb logcat | stdbuf -oL grep USEFUL >> /Users/jianjia/Desktop/tmp/useful_info.txt &

# recode the metadata of miniapps during search
adb logcat | stdbuf -oL grep e7-FTSSOSHomeWebViewUI >> /Users/jianjia/Desktop/tmp/meta_data.txt &

source myenv/bin/activate
# start miniapp keyword search in wechat
python src/batchSearchInto.py