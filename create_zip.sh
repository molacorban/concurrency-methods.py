QUANTIDADE_DE_ARQUIVOS=$1
SEED=$2

for i in `seq $QUANTIDADE_DE_ARQUIVOS`
do
    echo $i
    cp "$SEED" "$SEED"_"$i".to_zip
done

zip resources/example.zip resources/*.to_zip
