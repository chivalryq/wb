pid=`cat run.pid`
echo ${pid}
kill -9 ${pid}
deactive
source env/bin/activate
gunicorn app:app -b 0.0.0.0:5678 -w 4 -p run.pid
