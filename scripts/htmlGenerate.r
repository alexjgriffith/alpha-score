#!/usr/bin/env R
#
# This file is part of peakAnalysis,
# http://github.com/alexjgriffith/alpha-score/, 
# and is Copyright (C) University of Ottawa, 2015. It is Licensed under 
# the three-clause BSD License; see LICENSE.txt.
# Author : Alexander Griffith
# Contact: griffitaj@gmail.com
#
#
######################################################################
######################################################################
#
# Usage:
#
# sets<-c("normal-abnormal_not_abnormal-normal.pwm",
#         "abnormal-normal_not_normal-abnormal.pwm",
#         "abnormal_normal-other_not_other-abnormal_normal.pwm")
# 

source("aux.r")
source("html.r")
require("seqLogo")

loadData<-function(fileLocation){
    data<-read.delim(fileLocation,header=FALSE,sep="\n")    
    out<-list()
    n<-0
    name<-c()
    for(i in seq(length(t(data)))){
        if(  ">" %in% strsplit(as.character(data[i,]),"")[[1]])
            {if (! n==0){out<-append(out,list(matrix(box,dim(box))))}
             box<-c()
             name<-c(name,strsplit(as.character(data[i,]),"\t")[[1]][1])
             n<-n+1}
        else{
            box<-rbind(box,(as.numeric(unlist(strsplit(as.character(data[i,]),"\t")))))}}
    cbind(name=name,data=append(out,list(matrix(box,dim(box)))))}

palindrome<-function(data){
    makePWM(t(apply(apply(data@pwm,2,rev),1,rev)))}

getScore<-function(pScore,motif,name){
    as.numeric(unlist(pScore[name]))[which(as.character(pScore$motif)==motif)[1]]}

imageList<-function(fileLocatoin,sets,x,shortNames,imageDirectory,front="motif_"){
    data<-loadData(paste(fileLocation,sets[x],sep=""))
    name<-shortNames[x]
    apply(data,1,function(x){htmlImage(paste(imageDirectory,front,name,"_",strsplit(x[1]$name,">")[[1]][2],".png",sep=""),"style","width:101px;height:50px")})}

scoreList<-function(fileLocatoin,sets,j,shortNames,i,pScoreFile){
    pScore<-read.table(pScoreFile,header=1)
    data<-loadData(paste(fileLocation,sets[j],sep=""))    
    apply(data,1,function(x){getScore(pScore,x[1]$name,shortNames[i])})}

getMotifs<-function(data){
    apply(data,1,function(x){strsplit(x$name,">")[[1]][2]})}

prepareTable<-function(loadData,fileLocation,sets,pScoreFile,x){
    apply(
        cbind(
            getMotifs(loadData(paste(fileLocation,sets[x],sep=""))),
            scoreList(fileLocation,sets,x,shortNames,1,pScoreFile),
            scoreList(fileLocation,sets,x,shortNames,2,pScoreFile)),
            #scoreList(fileLocation,sets,x,shortNames,3,pScoreFile)),
        1,function(x){htmlTable(matrix(collapse(as.character(x))),anotations=buildAnotations("style","font-size:10px"))})}

getFrameChar<-function(lis,val){
    as.character(lis[val][[1]])}

sequenceGen<-function(... ,fn, n=3){
    I<-lapply(seq(n),function(x) {fn( x=x,...)})
    ma<-max(sapply(I,length))
    I<-mapply( function(x,y){c(y,rep("",x))},ma-sapply(I,length),I)
    I<-data.frame(I)
    colnames(I)<-shortNames
    I}

printFasta<-function(fileLocation,sets,shortNames,imageDirectory)
    for(j in seq(length(sets))){
        data<-loadData(paste(fileLocation,sets[j],sep=""))
        a<-lapply(seq(length(data[,1])), function(i){makePWM(t(as.matrix(data[i,2]$data)))})
        for( i in seq(length(a))) {
            name<-shortNames[j]
            motif<-strsplit(data[i,1]$name,">")[[1]][2]
            png(paste(imageDirectory,"motif_p_",name,"_",motif,".png",sep=""))
            seqLogo(palindrome(a[[i]]),ic.scale=FALSE,xaxis=FALSE,yaxis=FALSE)
            dev.off()
            png(paste(imageDirectory,"motif_",name,"_",motif,".png",sep=""))
            seqLogo(a[[i]],ic.scale=FALSE,xaxis=FALSE,yaxis=FALSE)
            dev.off()}}

htmlGenerateMain<-function(fileLocation,sets,shortNames,imageDirectory,n=3){
    I<-sequenceGen(fn=imageList,n=n,fileLocation,sets,shortNames,imageDirectory)
    IP<-sequenceGen(fn=imageList,n=n,fileLocation,sets,shortNames,imageDirectory,front="motif_p_")
    M<-sequenceGen(fn=prepareTable,n=n,loadData,fileLocation,sets,pScoreFile)
    mat<-matrix(unlist(lapply(seq(n),function(x){lapply(list(I,IP,M),getFrameChar,x)})),ncol=6)
    htmlDoc(htmlTags("head",htmlTags("title", "Test Images")),htmlTags("body",c(htmlTable(mat))))}

sets<-c("normal_not_normal.pwm", "abnormal_not_abnormal.pwm")
 shortNames<-c("n_not_n","a_not_a")
 fileLocation<-"~/Dropbox/temp-data/"
 pScoreFile<-"/home/agriffith/Dropbox/temp-data/p-score_table_1.tab"
 imageDirectory="/home/agriffith/Dropbox/temp-data/"
 printFasta(fileLocation,sets,shortNames,imageDirectory)
 write(htmlGenerateMain(fileLocation,sets,shortNames,imageDirectory,n=2),
       "a-score_other.html")
