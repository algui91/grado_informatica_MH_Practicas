s=385806854
s=1006087674
s=1492845388
s=691187430
s=665429938
s=3264321546 # 8 desv sa

s=$(od -vAn -N4 -tu4 < /dev/urandom)

# para genético
s=2982036107
s=3587169482 # El nug25 casi llega al optimo con esta 
s=1411423505 # Nug a 3764 de 3744

s=$(od -vAn -N4 -tu4 < /dev/urandom)

ficheros="els19.dat chr20a.dat chr25a.dat nug25.dat bur26a.dat bur26b.dat tai30a.dat tai30b.dat esc32a.dat kra32.dat tai35a.dat tai35b.dat tho40.dat tai40a.dat sko42.dat sko49.dat tai50a.dat tai50b.dat tai60a.dat lipa90a.dat"
s=3327229832
echo -e "seed=$s\n\n\n"

echo "10_1"

for i in $ficheros
do
    python QAP.py -d "data/"$i -a ma_10_1_pmx -s $s
done

echo -e "\n\n\n01\n\n\n"

for i in $ficheros
do
    python QAP.py -d "data/"$i -a ma_10_01_pmx -s $s
done

echo -e "\n\n\n01_best\n\n\n"

for i in $ficheros
do
    python QAP.py -d "data/"$i -a ma_10_01best_pmx -s $s
done
