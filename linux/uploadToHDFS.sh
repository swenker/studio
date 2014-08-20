#!/bin/sh

# upload log file to hdfs

date_yesterday=`date --date '1 days ago' +%Y%m%d`
echo $date_yesterday

local_files_qasvc="/home/clog/mcilog/*-qasvc*_$date_yesterday*.zip"
local_files_stsvc="/home/clog/mcilog/*-stsvc*_$date_yesterday*.zip"
local_files_svc="/home/clog/mcilog/*-svc*_$date_yesterday*.zip"

#`ls $local_files_qasvc`

HADOOP_HOME="/data/hadoop/hadoop-2.2.0"
`$HADOOP_HOME/bin/hadoop fs -put $local_files_qasvc /data/smagazine/logs/3m-server/qasvc/`
#`$HADOOP_HOME/bin/hadoop fs -put $local_files_stsvc /data/smagazine/logs/3m-server/stsvc/`
`$HADOOP_HOME/bin/hadoop fs -put $local_files_svc /data/smagazine/logs/3m-server/svc/`
`$HADOOP_HOME/bin/hadoop fs -put $local_files_svc /data/smagazine/logs/3m-server/stsvc/`
`$HADOOP_HOME/bin/hadoop fs -chmod -R o+w /data/smagazine/logs/3m-server/`

`mv $local_files_qasvc /home/clog/mcilog/archived/`
`mv $local_files_stsvc /home/clog/mcilog/archived/`
`mv $local_files_svc /home/clog/mcilog/archived/`

echo "--finished--"

