#!/data/binaries/R-3.1.0/bin/Rscript
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

loadProject<-function(projectDirectory,files,relative=TRUE){
    tempDir<-getwd()
    args <- commandArgs(trailingOnly = F)
    scriptDir<-dirname(sub("--file=","",args[grep("--file",args)]))
    setwd(scriptDir)
    for(file in files){
        source(paste(projectDirectory,file,sep=""),chdir=TRUE)}
    setwd(tempDir)}


######################################################################
######################################################################

library('getopt')
loadProject("../src/r/","pcaAnalysis.r")

spec = matrix(c(
    'fileLocation','i', 1,"character",
    'catagories','c', 1,"character",
    'cols','b', 1,"character"
    ),byrow=TRUE,ncol=4)
args=getopt(spec)

rootFile<-args$fileLocation
catFile<-args$catagories

values<-loadData(rootFile)
cats<-t(read.table(catFile))
data<-values$data
normData<-standPCAPrep(data,"colQn")
pcs<-prcomp(t(normData))

write.table(pcs$rotation[,as.numeric(strsplit(args$cols,",")[[1]])],stdout(),col.names=FALSE,row.names=FALSE,quote=FALSE,sep="\t")
