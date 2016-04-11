#!/usr/bin/env bash
ps -ef|grep uwsgi|grep -v grep|awk '{print $2}'|sort -n|head -1|xargs kill -9