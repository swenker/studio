
JAVA_HOME=/usr/java/current
export JAVA_HOME

PATH=$JAVA_HOME/bin:$PATH
export PATH

CATALINA_HOME=/usr/webserver/current
export CATALINA_BASE=/data/mscc/tomcat/webp
JAVA_OPTS="-server -Xms1536m -Xmx4096m -XX:NewSize=320m -XX:MaxNewSize=320m -XX:PermSize=96m -XX:MaxPermSize=256m -Xmn500m"

$CATALINA_HOME/bin/shutdown.sh

