#!/bin/bash

#download file from remote to test the download speed
#set -e

speed=$1
url=$2
status_file=$3
#speed=700
speedk="${speed}k"
#timeout=90
#url="http://dl-mas.svc.mcitech.cn/media/mas/app/4g/gaode_map/Samsung_S5_V7.2.1168.1452.0134_20140126.apk"


content_length=$(curl -sI $url | grep Content-Length | awk '{ print $2 }'| sed -e 's///g')
#content_length=$1
#echo "len:$content_length"
pre_spent=$(($content_length / $speed /1024))
timeout=$(($pre_spent*2))

#echo "${pre_spent},${timeout}"
#echo "download started...."
current_time=`date +%s`
#sleep 2
if [ -z $4 ] ;then
    #echo "production mode"
    curl -s --limit-rate ${speedk} -o ${status_file}_dl -m ${timeout} ${url}
fi

new_time=`date +%s`
spent=$(($new_time-$current_time))
size_in_m=$((${content_length}/1024/1024))

#write this to a file so that it can be retrieved by nrpe asynchronizously.
echo "$?#Downloaded ${size_in_m}M by ${speedk}/s in ${spent}seconds |${spent}" >${status_file}



exit 0

