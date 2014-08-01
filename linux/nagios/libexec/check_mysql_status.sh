#!/bin/sh 

STATE_OK=0
STATE_WARNING=1
STATE_CRITICAL=2
STATE_UNKNOWN=3 
STATUS_TXT='OK'
STATUS_CODE=$STATE_OK

CRITICAL_VALVE=350
WARN_VALVE=100

HOSTA=''
dbuser=''
dbpasswd=''

while getopts "H:u:p:c:w:s:" opt; do
    case $opt in
        H)
            HOSTA=$OPTARG
            ;;
        u)
            dbuser=$OPTARG
            ;;
        p)
            dbpasswd=$OPTARG
            ;;  
        c)
           CRITICAL_VALVE=$OPTARG
           ;;
        w) 
           WARN_VALVE=$OPTARG
           ;;

        s)
           statem=$OPTARG ;;

        *)
            echo "Invalid option"
            exit
    esac
done

TCounter=0
#let results=$(mysql -u$dbuser -p$dbpasswd -h$HOSTA  -e "$statem"|wc -l)
 TCounter=$(mysql -u$dbuser -p$dbpasswd -h$HOSTA  -e "SHOW STATUS WHERE \`variable_name\` = 'Threads_connected'" |grep Threads_connected|awk '{print $2}')
#echo $results
#echo "$statem;;$results"

if [ $TCounter -ge $CRITICAL_VALVE ]; then
      STATUS_TXT="Critical"
      STATUS_CODE=2
elif [ $TCounter -ge $WARN_VALVE ]; then
      STATUS_TXT="Warning"
      STATUS_CODE=1
fi

echo "$STATUS_TXT -$TCounter|TC=$TCounter;100;350;1;450" 
exit $STATUS_CODE

