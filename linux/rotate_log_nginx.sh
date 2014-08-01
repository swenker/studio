#!/bin/bash

declare -a log_path
#log_path=("/data/applog/nginx/mas/" "/data/applog/nginx/mainaccess/")
log_path[0]="/data/applog/nginx/mas/" 
log_path[1]="/data/applog/nginx/mainaccess/"
log_path[2]="/data/applog/nginx/3m/"


for daily_log_path in ${log_path[@]} ; do
    rt_log_path=${daily_log_path}
    echo ${rt_log_path}
    mv ${rt_log_path}access.log ${daily_log_path}access_$(date -d "yesterday" +%Y%m%d).log
done

nginx_pid=`ps aux |grep -E 'nginx: master process'|grep -v 'grep'|awk '{print $2}'`
kill -USR1 $nginx_pid 

service nginx reload
