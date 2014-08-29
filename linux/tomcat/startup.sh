JAVA_HOME=/usr/java/current
export JAVA_HOME

PATH=$JAVA_HOME/bin:$PATH
export PATH

CATALINA_HOME=/usr/webserver/current
export CATALINA_BASE=/data/mscc/tomcat/webp

JAVA_OPTS="-javaagent:$CATALINA_BASE/sflowagent.jar -server -Xms1536m -Xmx4096m -XX:NewSize=320m -XX:MaxNewSize=320m -XX:PermSize=96m -XX:MaxPermSize=256m -Xmn500m"
JAVA_OPTS="$JAVA_OPTS -XX:ErrorFile=/data/mscc/hs_err_pid.log -XX:+HeapDumpOnOutOfMemoryError -XX:HeapDumpPath=/data/mscc/java_pid.hprof"
echo $JAVA_OPTS

export JAVA_OPTS

$CATALINA_HOME/bin/startup.sh

