s=$RANDOM

for i in `ls data/*.dat`
do
    python QAP.py -d $i -a local_search -s $s
done
