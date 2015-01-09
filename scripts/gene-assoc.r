#!/usr/bin/env R
#
# This file is part of peakAnalysis,
# http://github.com/alexjgriffith/alpha-score/, 
# and is Copyright (C) University of Ottawa, 2015. It is Licensed under 
# the three-clause BSD License; see LICENSE.txt.
# Author : Alexander Griffith
# Contact: griffitaj@gmail.com
#
#######################################################################
######################################################################
#
# Usage:
#
# fileLocation="~/Dropbox/UTX-Alex/jan/"
# bedData<-read.delim(paste(fileLocation,"combined_sorted.bed",sep=""),header=0)
# geneList<-read.delim(paste(fileLocation,"hg19.RefSeqGenes.csv",sep=""))
# genes<-geneAssociation(bedData,geneList,  c(50000,0,0,0))
# write.table(cbind(bedData,unlist(t(lapply(genes, function(x) {if(identical(x,character(0))){"None"} else{x}})))) ,"combined_tagged_genes.bed" ,col.names=FALSE,row.names=FALSE,quote=FALSE,sep="\t")

member<-function(posibList,mem,test="default"){
    fun<-switch(test,default=function(x,y){all(y %in% x)})
    sapply(posibList,fun,mem)}

memberWrapper<-function(bedData,lis ,n=4,sep="-"){
    member(strsplit(as.character(bedData[,n]),sep),lis)}

geneAssoc<-function(point,geneList,bounds){
    # Currently Returns the enhancer locations
    peak<-(as.numeric(point[[2]])+as.numeric(point[[3]]))/2
    tss<-geneList$txStart
    ess<-geneList$txEnd
    chrom<-geneList$chrom
    a<-which(chrom==as.character(point[[1]]))
    b<-a[which(tss[a]-bounds[1]<peak)]
    r<-b[which(ess[b]+bounds[3]>peak)]
    e<-r[c(which(tss[r]-bounds[2]>peak),which(ess[r]+bounds[4]<peak))]
    e}
       
minGene<-function(x,y,start,miz=1){
    x[which(order(abs(start[x]-y))<=miz)]}

geneAssociation<-function(bedData,geneList,bounds,miz=1){
    locations<-apply(bedData,1,function(x){geneAssoc(x,geneList,bounds)})
    peak<-(as.numeric(bedData[,2])+as.numeric(bedData[,3]))/2
    tssGenes<-mapply(minGene,locations,peak,
                     MoreArgs=list(start=geneList$txStart,miz=miz))
    lapply(tssGenes, function(x){as.character(geneList$name2[x])})}
