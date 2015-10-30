ficheros="esc64a esc128 lipa90b sko64 sko72 sko81 sko90 sko100a tai64c tai80a"

s=12345678

echo -e "seed=$s\n\n\n"

for i in $ficheros
do
    python QAP.py -d "Competición/"$i".dat" -a CompPob -s $s
done
