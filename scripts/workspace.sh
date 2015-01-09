#!/bin/bash
#
# This file is part of peakAnalysis,
# http://github.com/alexjgriffith/alpha-score/, 
# and is Copyright (C) University of Ottawa, 2015. It is Licensed under 
# the three-clause BSD License; see LICENSE.txt.
# Author :Alexander Griffith
# Contact: griffitaj@gmail.com

abnormal="jurk\|rpmi\|cem\|tall_p1\|tall_p2\|tall_p3"
normal="k562\|eryt"
stem="cd133\|cd34"
other="cd133\|cd34\|meka\|ecfc"

combine(){ paste $1"_sorted.bed" <(grep -v ">" "$1".fasta|sed 's/^.//g');}
makeFasta(){ awk '{print ">"$1":"$2"-"$3"\n"$5}';}

for i in `echo normal-abnormal abnormal-normal`
do
eval $(echo -e $i | awk -F "-" '{print "/data/binaries/homer/bin/homer2 denovo -i <(combine combined| ./select.sh -f $"$1" -b $"$2") -b <(combine combined| ./select.sh -b $"$1" -f $"$2") -len 6 -o "$1"-"$2"_not_"$2"-"$1}')
done

i="abnormal-normal"
eval $(echo -e $i | awk -F "-" '{print "/data/binaries/homer/bin/homer2 denovo -i <(combine combined|grep  -v $other |makeFasta) -b <(combine combined|grep $other |makeFasta) -len 6 -o "$2"_"$1"_not_other.pwm"}')

#sets=`echo -e "abnormalNormal-stem_not_abnormalNormal-stem.pwm" "stem-abnormalNormal_not_stem-abnormalNormal.pwm" "normalStem-abnormal_not_normalStem-abnormal.pwm" "abnormal-normalStem_not_abnormal-normalStem.pwm" "normal-abnormalStem_not_normal-abnormalStem.pwm" "abnormalStem-normal_not_abnormalStem-normal.pwm"`
#fileLocation=/mnt/brand01-00/mbrand_analysis/projects/august/data/motifpeaks/

fileLocation=/home/griffita/Dropbox/UTX-Alex/jan/
sets=("normal-abnormal_not_abnormal-normal" "abnormal-normal_not_normal-abnormal" "abnormal_normal-other_not_other-abnormal_normal")
files=`echo ${sets[*]}| sed 's/\ /\n/g'| awk '{print $1".pwm"}'`


for i in ${sets[*]}
do
    cp `echo $i | awk -v f=$fileLocation  '{print f$1".pwm"}'` ~/Dropbox/temp-data/
done

#for  i in $sets 
#do
#    cp $fileLocation$i ~/Dropbox/temp-data/
#done

set +o posix
#loc=/mnt/brand01-00/mbrand_analysis/projects/august/data/motifpeaks/



#for j in $files
#do
#for i in $files
#do
#outfile=$(echo "" | awk -v a=`echo $j | sed 's/.pwm//g'`  -v b=`echo $i | sed 's/.pwm//g' ` '{print a","b}' | sed -r 's/Stem|stem/s/g;s/Abnormal|abnormal/n/g;s/Normal|normal/a/g;')
#a=`echo $i |sed 's/.pwm//g' | sed 's/_not_/\tnot_/g'`
#b=`echo $a | awk -v loc=$loc -v m=$j '{print " -i "loc$1"_peaks.fasta -b "loc$2"_peaks.fasta -m " m}'`
#echo $b
#/data/binaries/homer/bin/homer2 known `echo $b` >motif-analysis/$outfile
#done
#done




for j in $files
do
for i in $files
do
fastaFile=$(echo $i |awk -F "_not_" '{ print $1}'| sed 's/.pwm//' | awk -F "-"  -v type="combined" '{print "combine ../UTX-Alex/jan/"type"  |grep $(eval $(echo  \"echo $\""$1" | sed \x27s/_/\"""\\\\\\\\""|\"$/g\x27)) | grep -v $(eval $(echo  \"echo $\""$2" | sed \x27s/_/\"""\\\\\\\\""|\"$/g\x27))|makeFasta"}')
backFile=$(echo $i |awk -F "_not_" '{ print $2}'| sed 's/.pwm//' | awk -F "-"  -v type="combined" '{print "combine ../UTX-Alex/jan/"type"  |grep $(eval $(echo  \"echo $\""$1" | sed \x27s/_/\"""\\\\\\\\""|\"$/g\x27)) |grep -v $(eval $(echo  \"echo $\""$2" | sed \x27s/_/\"""\\\\\\\\""|\"$/g\x27))|makeFasta"}')
outfile=$(echo "" | awk -v a=`echo $j | sed 's/.pwm//g'`  -v b=`echo $i | sed 's/.pwm//g' ` '{print a","b}' | sed -r 's/other/o/g;s/Stem|stem/s/g;s/Abnormal|abnormal/n/g;s/Normal|normal/a/g;')
echo $outfile
/data/binaries/homer/bin/homer2 known  -i <(eval $(echo $fastaFile)) -b <(eval $(echo $backFile)) -m $j  >motif-analysis/$outfile
wc -l motif-analysis/$outfile
done
done


echo -e "motif\tn\ta\tan">temp3
for j in $files
do
grep ">" $j | cut -f 1 > temp
for i in $files
do
outfile=$(echo "" | awk -v a=`echo $j | sed 's/.pwm//g'`  -v b=`echo $i | sed 's/.pwm//g' ` '{print a","b}' | sed -r 's/other/o/g;s/Stem|stem/s/g;s/Abnormal|abnormal/n/g;s/Normal|normal/a/g;')
echo $outfile
paste temp <(awk 'NR>1{print $3}' motif-analysis/$outfile) >temp2
mv temp2 temp
done
cat temp3 temp >temp4
mv temp4 temp3
done

sed -r 's/1e|1e-//g' temp3 > p-score_table.tab

/data/binaries/homer/bin/homer2 known -i /mnt/brand01-00/mbrand_analysis/projects/august/data/motifpeaks/normal-abnormalStem_peaks.fasta -b /mnt/brand01-00/mbrand_analysis/projects/august/data/motifpeaks/abnormalStem-normal_peaks.fasta -m normal-abnormalStem_not_normal-abnormalStem.pwm 



