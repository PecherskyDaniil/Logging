PID1=`ps -a|grep uvicorn`
kill ${PID1:2:6}
PID2=`ps -a|grep python3| sed -n '$p' -`
kill ${PID2:2:6}
PID3=`ps -a|grep python3| sed -n '$p' -`
kill ${PID3:2:6}