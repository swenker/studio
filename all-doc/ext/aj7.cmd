echo "set JAVA_HOME-7, MVN_HOME,ANDROID_HOME and their related paths"
echo off
set MVN_HOME=D:\work\tools\apache-maven-3.0.5
set ANDROID_HOME=D:\work\tools\sdk
SET JAVA_HOME=D:\work\tools\jdk1.7.0_25
PATH=%JAVA_HOME%\bin;%MVN_HOME%\bin;%ANDROID_HOME%\platform-tools;%PATH%;C:\Python27;D:\work\tools\svn-win32-1.6.23\bin;C:\Program Files\OpenVPN\bin
set PYTHONPATH=%PYTHONPATH%;D:\work\projects\111-tech-bmlist\bmlist

echo on