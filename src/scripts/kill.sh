#!/bin/sh
killall -2 server.py 
sleep 1
killall -2 monitor.py
killall -2 client.py
runing=`ps -aux | grep -E "monitor.py|server.py|client.py" | wc -l`
echo ${running}
sleep 2
ps -aux | grep -E "monitor.py|server.py|client.py"
killall -9 server.py monitor.py client.py
