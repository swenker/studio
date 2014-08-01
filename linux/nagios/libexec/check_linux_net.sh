#!/bin/sh
IF=''
output='MB'
CRITICAL_VALVE=100
WARN_VALVE=50

while getopts "i:o:c:w:" opt; do
    case $opt in
        i)
            IF=$OPTARG
            ;;
        o)
            output=$OPTARG
            ;;
        c)
           let CRITICAL_VALVE=$OPTARG*1024*1024
           ;;
        w) 
           let  WARN_VALVE=$OPTARG*1024*1024
           ;;

        *)
            echo "Invalid option"
            exit 3 #Unknown
    esac
done

if [ -z "$IF" ]; then
        IF=`ls -1 /sys/class/net/ | head -1`
fi

RXPREV=-1
TXPREV=-1
#echo "Listening $IF... $output,$CRITICAL_VALVE,$WARN_VALVE"

STATUS_TXT='OK'
STATUS_CODE=0
while [ 1 == 1 ] ; do
        RX=`cat /sys/class/net/${IF}/statistics/rx_bytes`
        TX=`cat /sys/class/net/${IF}/statistics/tx_bytes`
        if [ $RXPREV -ne -1 ] ; then
            let bytes_in=$RX-$RXPREV
            let bytes_out=$TX-$TXPREV
            return_bytes_in=$bytes_in
            return_bytes_out=$bytes_out
                
                # In case KB or MB has been set in -o option
            if [ -n "${output}" ] ;  then
 
                  if [ "${output}" = "KB" ]; then
                        return_bytes_in=$(expr ${bytes_in} / 1024)
                        return_bytes_out=$(expr ${bytes_out} / 1024)
                        value="KBytes"
                  elif [ "${output}" = "MB" ]; then 
                        return_bytes_in=$(expr ${bytes_in} / 1024 / 1024)
                        return_bytes_out=$(expr ${bytes_out} / 1024 / 1024)
                        value="MBytes"
                  fi
            else
                  return_bytes_in=${bytes_in}
                  return_bytes_out=${bytes_out}
                  value="Bytes"
            fi

                 
           # if [ [ $bytes_out -ge $WARN_VALUE ] -a [ $bytes_out -lt $CRITICAL_VALUE ] ]; then
            if [ $bytes_out -ge $CRITICAL_VALVE ]; then
                  STATUS_TXT="Critical"
                  STATUS_CODE=2

            elif [ $bytes_out -ge $WARN_VALVE ]; then
                  STATUS_TXT="Warning"
                  STATUS_CODE=1
            fi

            # Output
            echo "Network ${STATUS_TXT} - ${return_bytes_in} ${value} received/sec, ${return_bytes_out} ${value} sent/sec|bytes_in=${bytes_in};bytes_out=${bytes_out}"

#               echo "Network OK - $R_RX K Bytes received/sec, $R_TX K Bytes sent/sec|bytes_in=$R_RX;bytes_out=$R_TX"
            exit $STATUS_CODE
        fi
        RXPREV=$RX
        TXPREV=$TX
        sleep 1
done

