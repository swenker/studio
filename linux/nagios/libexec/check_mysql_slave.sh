#!/bin/sh 
declare -a    slave_is 

STATE_OK=0
STATE_WARNING=1
STATE_CRITICAL=2
STATE_UNKNOWN=3 

HOSTA=''
dbuser=''
dbpasswd=''
while getopts "H:u:p:c:w" opt; do
    case $opt in
        H)
            HOSTA=$OPTARG
#            echo "project name is [$project_name]"
            ;;

        u)
            dbuser=$OPTARG
            ;;
        p)
            dbpasswd=$OPTARG
            ;;  
        c)
           ;;
        w) ;;

        *)
            echo "Invalid option"
            exit
    esac
done

slave_is=($(mysql -u$dbuser -p$dbpasswd -h$HOSTA  -e "show slave status\G"|grep Running |awk '{print $2}')) 
#echo $slave_is
if [ "${slave_is[0]}" = "Yes" -a "${slave_is[1]}" = "Yes" ] 
     then 
     echo "OK -slave is running" 
     exit $STATE_OK
else 
     echo "Critical -slave is error" 
     exit $STATE_CRITICAL 
fi 

