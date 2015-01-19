#!/bin/bash
#
# This file is part of peakAnalysis,
# http://github.com/alexjgriffith/alpha-score/, 
# and is Copyright (C) University of Ottawa, 2015. It is Licensed under 
# the three-clause BSD License; see LICENSE.txt.
# Author :Alexander Griffith
# Contact: griffitaj@gmail.com

Rscript scripts/a-score.r -i ~/Dropbox/UTX-Alex/jan/combined_heights.bed -c ~/Dropbox/UTX-Alex/jan/catagories -b 1,3,8
