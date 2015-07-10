#!/bin/sh

PROGRAM="effectMonitor"

while true
do
	pro_num=`ps aux | grep $PROGRAM | grep -v grep | wc -l`	
	if [ $pro_num -lt 1 ];then
		d=`date +%Y%m%d%H%M%S`
		echo "restart on $d" >> ./log/run.log	
		nohup ./effectMonitorMain.py >> ./log/run.log 2>&1 &
	fi
	sleep 10
done
exit 0
