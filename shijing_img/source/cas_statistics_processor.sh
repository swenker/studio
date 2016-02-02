#!/usr/bin/env bash

yesterday_underscore=`date -d 'yesterday' +%Y_%m_%d`
yesterday_minus=`date -d 'yesterday' +%Y-%m--%d`
result_file=cas_result_$yesterday_underscore

ssh -t pe-mmi.chinacloudapp.cn "python ~/collect_cas_request.py www.motorola.com.cn $yesterday_underscore"

scp pe-mmi.chinacloudapp.cn:~/$result_file /home/wenjusun/work/cas-statistics/

requests_result=`cat /home/wenjusun/work/cas-statistics/$result_file`

python /home/wenjusun/studio/studio/shijing_img/source/handle_cas_statistics.py $yesterday_underscore $requests_result


