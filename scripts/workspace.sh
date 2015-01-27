#!/bin/bash
#
# This file is part of peakAnalysis,
# http://github.com/alexjgriffith/alpha-score/, 
# and is Copyright (C) University of Ottawa, 2015. It is Licensed under 
# the three-clause BSD License; see LICENSE.txt.
# Author :Alexander Griffith
# Contact: griffitaj@gmail.com

set +o posix

abnormal="jurk\|rpmi\|cem\|tall_p1\|tall_p2\|tall_p3"
normal="k562\|eryt"
stem="cd133\|cd34"
other="cd133\|cd34\|meka\|ecfc"


python2.7 scripts/tags2.py <(paste  <(cut -f 1-3 ~/Dropbox/UTX-Alex/jan/combined_heights.bed) <(grep -v ">" ~/Dropbox/UTX-Alex/jan/combined.fasta) <(Rscript scripts/a-score.r -i ~/Dropbox/UTX-Alex/jan/combined_heights.bed -c ~/Dropbox/UTX-Alex/jan/catagories -b 1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20)) >/home/agriffith/Dropbox/UTX-Alex/jan/combined_scored.bed

python2.7 scripts/tags2.py <(paste  <(cut -f 1-4 ~/Dropbox/UTX-Alex/jan/combined_sorted.bed)  <(cut -f 1 ~/Dropbox/UTX-Alex/jan/combined_scored.bed)) top | grep -v ">" | grep <(echo  $abnormal) | wc -l

python2.7 scripts/assesTags.py <(paste  <(cut -f 1-4 ~/Dropbox/UTX-Alex/jan/combined_sorted.bed )  <(awk 'NR>1{print $1}' ~/Dropbox/UTX-Alex/jan/combined_scored.bed)) top 3
