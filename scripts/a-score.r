#!/data/binaries/R-3.1.0/bin/Rscript
library('getopt')
source("pcaAnalysis.r")

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
