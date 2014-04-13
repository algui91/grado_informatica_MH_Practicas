s=385806854
s=1006087674
s=1492845388
s=691187430
s=665429938
s=3264321546 # 8 desv sa

s=$(od -vAn -N4 -tu4 < /dev/urandom)

s=3264321546 # 8 desv sa
ficheros="els19.dat chr20a.dat chr25a.dat nug25.dat bur26a.dat bur26b.dat tai30a.dat tai30b.dat esc32a.dat kra32.dat tai35a.dat tai35b.dat tho40.dat tai40a.dat sko42.dat sko49.dat tai50a.dat tai50b.dat tai60a.dat lipa90a.dat"

echo -e "seed=$s\n\n\n"

for i in $ficheros
do
    python QAP.py -d "data/"$i -a local_search -s $s
done

echo -e "\n\n\n\n\n\n\n"

for i in $ficheros
do
    python QAP.py -d "data/"$i -a sa -s $s
done
echo -e "\n\n\n\n\n"
for i in $ficheros
do
    python QAP.py -d "data/"$i -a greedy -s $s
done
