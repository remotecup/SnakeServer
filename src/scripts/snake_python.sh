#!/bin/sh
rundir=`pwd`
echo ${rundir}
cd ..
./server.py > /dev/null 2>&1 &
./client.py -c greedy -n greedy1 > /dev/null 2>&1 &
./client.py -c best -n best > /dev/null 2>&1 &
./client.py -c greedy -n greedy2 > /dev/null 2>&1 &
./client.py -c your -n yourSnake > /dev/null 2>&1 &
./monitor.py > /dev/null 2>&1 &
cd ${rundir}

