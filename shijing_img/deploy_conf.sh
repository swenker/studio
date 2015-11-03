#!/bin/sh

config_set=$1

cp conf/${config_set}/*.cfg /var/shijing/conf
cp conf/Abyssinica_SIL.ttf /var/shijing

echo "Done for--------${config_set}."

