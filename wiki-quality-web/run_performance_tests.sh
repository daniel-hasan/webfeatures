python3 run_scheduler.py createdb $1 $2

for (( i=1; i <= $2; ++i ))
do
    echo "runing $i..."
    python3 run_scheduler.py runscheduler $1 $2>>output_$i&
done
