#!/bin/sh
while true
 do
   DD_SITE="datadoghq.com" DD_API_KEY=$1 python3 "custom_metric.py"
   sleep 60;
 done
