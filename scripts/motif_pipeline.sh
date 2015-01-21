#!/bin/bash
#
# This file is part of peakAnalysis,
# http://github.com/alexjgriffith/alpha-score/, 
# and is Copyright (C) University of Ottawa, 2015. It is Licensed under 
# the three-clause BSD License; see LICENSE.txt.
# Author :Alexander Griffith
# Contact: griffitaj@gmail.com

# Environment
set +o posix
combine(){ paste $1"_sorted.bed" <(grep -v ">" "$1".fasta|sed 's/^.//g');}
makeFasta(){ awk '{print ">"$1":"$2"-"$3"\n"$5}';}

# Shorthands
abnormal="jurk\|rpmi\|cem\|tall_p1\|tall_p2\|tall_p3"
normal="k562\|eryt"
stem="cd133\|cd34"
other="cd133\|cd34\|meka\|ecfc"

# Variables
fileLocation=/home/griffita/Dropbox/UTX-Alex/jan/
#sets=("normal-abnormal_not_abnormal-normal" "abnormal-normal_not_normal-abnormal" "abnormal_normal-other_not_other-abnormal_normal")
sets=("ecfc_not_ecfc")
files=`echo ${sets[*]}| sed 's/\ /\n/g'| awk '{print $1".pwm"}'`
transform='s/other/o/g;s/Stem|stem/s/g;s/Abnormal|abnormal/a/g;s/Normal|normal/n/g;s/Meka|meka/m/g;s/ECFC|ecfc/e/g;'
header=$(echo  ${sets[*]} | sed -r $(echo $transform) | awk '{print "motif " $0}' | sed 's/\ /\\t/g')


# Generate Fasta Files Based On Sets
for i in ${sets[*]}
do
    f1=`echo $i | sed 's/_not_/\t/g'| cut -f 1 | cut -f 1 -d "-"| awk '{print "echo $"$0}' |sed 's/_/\"\\\\\\\\|\"$/g'`
    b1=`echo $i | sed 's/_not_/\t/g'| cut -f 1 | cut -f 2 -d "-"| awk '{print "echo $"$0}' |sed 's/_/\"\\\\\\\\|\"$/g'`
    f2=`echo $i | sed 's/_not_/\t/g'| cut -f 2 | cut -f 1 -d "-"| awk '{print "echo $"$0}' |sed 's/_/\"\\\\\\\\|\"$/g'`
    b2=`echo $i | sed 's/_not_/\t/g'| cut -f 2 | cut -f 2 -d "-"| awk '{print "echo $"$0}' |sed 's/_/\"\\\\\\\\|\"$/g'`
    /data/binaries/homer/bin/homer2 denovo \
	-i <(combine combined | grep $(eval $f1) | grep -v $(eval $b1)| head |makeFasta) \
	-b <(combine combined | grep $(eval $f2) | grep -v $(eval $b2)| head |makeFasta) \
	-len 6 -o $i
done

Rscript ./scripts/a-score.r -i ~/Dropbox/UTX-Alex/jan/combined_heights.bed -c ~/Dropbox/UTX-Alex/jan/catagories -b 1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20 > ~/Dropbox/UTX-Alex/jan/combined_scored.bed

python2.7 ./scripts/tags2.py <(paste <( cut -f 1-3 ~/Dropbox/UTX-Alex/jan/combined_sorted.bed) <(grep -v ">" ~/Dropbox/UTX-Alex/jan/combined.fasta) <( cut -f 8 ~/Dropbox/UTX-Alex/jan/combined_scored.bed)) bottom > $fileLocation"meka.fasta"

for i in ${sets[*]}
do
a=$(echo $i |awk -F "_not_" '{print $1".fasta"}')
b=$(echo $i |awk -F "_not_" '{print "not_"$2".fasta"}')

/data/binaries/homer/bin/homer2 denovo -i $fileLocation$a -b $fileLocation$b -len 6 -o $fileLocation$i".pwm"
done

# Move the fasta files to an appopirate location
for i in ${sets[*]}
do
    cp `echo $i | awk -v f=$fileLocation  '{print f$1".pwm"}'` ~/Dropbox/temp-data/$i".pwm"
done

# Generate the count files (cross info for each file)
for j in $files
do
    for i in $files
    do
	fastaFile=`echo $i |awk -F "_not_" -v file=$fileLocation '{ print file$1".fasta"}'`
	#$(echo $i |awk -F "_not_" '{ print $1}'| sed 's/.pwm//' | awk -F "-"  -v type="combined" '{print "combine ../UTX-Alex/jan/"type"  |grep $(eval $(echo  \"echo $\""$1" | sed \x27s/_/\"""\\\\\\\\""|\"$/g\x27)) | grep -v $(eval $(echo  \"echo $\""$2" | sed \x27s/_/\"""\\\\\\\\""|\"$/g\x27))|makeFasta"}')
	backFile=`echo $i |awk -F "_not_" -v file=$fileLocation '{ print file"not_"$2}' | sed 's/.pwm/.fasta/'`
	#$(echo $i |awk -F "_not_" '{ print $2}'| sed 's/.pwm//' | awk -F "-"  -v type="combined" '{print "combine ../UTX-Alex/jan/"type"  |grep $(eval $(echo  \"echo $\""$1" | sed \x27s/_/\"""\\\\\\\\""|\"$/g\x27)) |grep -v $(eval $(echo  \"echo $\""$2" | sed \x27s/_/\"""\\\\\\\\""|\"$/g\x27))|makeFasta"}')
	outfile=$(echo "" | awk -v a=`echo $j | sed 's/.pwm//g'`  -v b=`echo $i | sed 's/.pwm//g' ` '{print a","b}' | sed -r $transform)
	echo $outfile
	#/data/binaries/homer/bin/homer2 known  -i <(eval $(echo $fastaFile)) -b <(eval $(echo $backFile)) -m $j  >motif-analysis/$outfile
	/data/binaries/homer/bin/homer2 known  -i $fastaFile -b $backFile -m $j  >motif-analysis/$outfile
	wc -l motif-analysis/$outfile
    done
done

# Genearate A table to be opened by R
echo -e $header>temp3
for j in $files
do
grep ">" $j | cut -f 1 > temp
for i in $files
do
outfile=$(echo "" | awk -v a=`echo $j | sed 's/.pwm//g'`  -v b=`echo $i | sed 's/.pwm//g' ` '{print a","b}' | sed -r $transform)
echo $outfile
paste temp <(awk 'NR>1{print $6}' motif-analysis/$outfile) >temp2
mv temp2 temp
done
cat temp3 temp >temp4
mv temp4 temp3
done

sed -r 's/1e|1e-//g' temp3 > e_not_e_p-score_table.tab
