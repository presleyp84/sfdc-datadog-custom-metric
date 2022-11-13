#!/bin/sh
DD_SITE="datadoghq.com" DD_API_KEY=$DD_API_KEY python3 "sample_dev.py"

 while true
 do
   DD_SITE="datadoghq.com" DD_API_KEY=$DD_API_KEY python3 "custom_metric.py"
   sleep 60;
 done
