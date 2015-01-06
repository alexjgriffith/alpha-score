#!/usr/bin/env R
#
# This file is part of peakAnalysis, http://github.com/alexjgriffith/alpha-score/, 
# and is Copyright (C) University of Ottawa, 2015. It is Licensed under 
# the three-clause BSD License; see LICENSE.txt.
# Contact: griffitaj@gmail.com


collapse<-function(...){paste(...,sep="")}
lcollapse<-function(x){br<-"";for(i in x){br<-paste(br,i,sep="")};br}
collect<-function(x,fn,...){lcollapse(sapply(x,fn,...))}
modulous<-function(x,m)
    {t1<-floor(x/m)
     (x-t1*m)}