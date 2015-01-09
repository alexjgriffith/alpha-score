#!/usr/bin/env R
#
# This file is part of peakAnalysis,
# http://github.com/alexjgriffith/alpha-score/, 
# and is Copyright (C) University of Ottawa, 2015. It is Licensed under 
# the three-clause BSD License; see LICENSE.txt.
# Author :Alexander Griffith
# Contact: griffitaj@gmail.com
#
#
######################################################################
######################################################################

strList<-"(intersection jurk cem rpmi (not (union k562 eryt)))"

subList<-list("union","jurk","cem","rpmi",list("not",list("union","k562","eryt")))

for(i in subList[2:length(subList)]){if(is.list(i)){print i}}

website<-htmlDoc(htmlTags("body",collapse(htmlTags("H1","Welcome"),
         htmlTags("p","This is a quick sample pagargaph"),
         htmlTable(matrix(c(1,2,3,4),2,2)))))
write(website,"test.html")

nb<-buildAnotations("cellpadding", "0")
cat(htmlTable(matrix(c(htmlTable(matrix(c(1,2,3),3,1),nb),htmlTable(matrix(c(1,2,3),3,1),nb),htmlTable(matrix(c(1,2,3),3,1),nb),htmlTable(matrix(c(1,2,3),3,1),nb)),2,2)))

matrix(list(list(1,2,3),list(1,2),list(1),list(1,2,3,4)),ncol=2)[1,1]

#allFasta<-readDNAStringSet(paste(fileLocation,"combined.fasta",sep=""),use.names=TRUE)
#foreg<-allFasta[member(strsplit(as.character(types[,4]),"-"),c("k562","eryt"))]
#backg<-allFasta[member(strsplit(as.character(types[,4]),"-"),c("jurk","cem","rpmi"))]
