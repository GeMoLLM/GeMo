set -x
for i in $(seq $6 $7);
do
    python merge.py --prefix goodreads_completions_$1_$2-nonchat_500_temp-$3_p-$4_k-$5-$i --n 5;\
done