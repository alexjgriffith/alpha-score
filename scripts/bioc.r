#!/usr/bin/env R
#
# This file is part of peakAnalysis, http://github.com/alexjgriffith/alpha-score/, 
# and is Copyright (C) University of Ottawa, 2015. It is Licensed under 
# the three-clause BSD License; see LICENSE.txt.
# Contact: griffitaj@gmail.com


#Aux Functions

#Logo generators
require("seqLogo")

getPWM<-function(motif,data){
    sets<-data$poisit[which(data$poisit==motif),]
    sets<-sets[order(sets[2]),3:length(sets[,1])]
    apply(sets,1,as.numeric)} 

printLogos<-function(data,shortName){
    for(i in data$name){
        x<-getPWM(i,data)
        logos<-makePWM(as.data.frame(x,row.names=c("A","B","C","D")))
        #png(paste("logo_",shortName,"_",gsub(">","",i),".png",sep=""),width=240,height=120)
        seqLogo(logos,xaxis=FALSE,yaxis=FALSE,ic.scale=FALSE)
        #dev.off()
        print(i)}}

fileLocation<-"/mnt/brand01-00/mbrand_analysis/projects/august/data/motifpeaks/"
sets<-c("normal-abnormalStem_not_normal-abnormalStem.pwm","abnormal-normalStem_not_abnormal-normalStem.pwm")
shortNames<-c("unormal","uabnormal")
data<-loadData(collapse(fileLocation,sets[1]))


data<-loadData("test.data")
motifs<-c()
for(j in seq(length(sets))){
    data<-loadData(paste(fileLocation,sets[j],sep=""))
    #printLogos(data,shortNames[j])
    motifs<-cbind(motifs,c(shortNames[j],data$name))}
motifs<-as.data.frame(t(as.data.frame(t(motifs[2:dim(motifs)[1],]), row.names=motifs[1,])))

br<-c()
for (i in seq(dim(a)[1]))
    {
        print(i)
        for (j in shortNames)
            print(j)
            print(motifs[j][i,1])
            br<-c(br,motifs[j][i,1], htmlTable(matrix(runif(3,0,1),3,1)))
    }
