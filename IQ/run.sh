for i in cft.csv ravens.csv surfdev.csv spacerel.csv readcomp.csv analogy.csv
do
    epd score.py $i {key_,data/scored_,out/item_,out/ttl_}$i
done
