#!/data/binaries/R-3.1/bin/Rscript
library('getopt')
source("gene-assoc.r")

spec = matrix(c(
    'fileLocation','d', 1,"character",
    'file','i', 1,"character"
    ),byrow=TRUE,ncol=4)
args=getopt(spec)

fileLocation=args$fileLocation 
bedData<-read.delim(paste(fileLocation,args$file,sep=""),header=0)    
geneList<-read.delim("../info/hg19.RefSeqGenes.csv")
genes<-geneAssociation(bedData,geneList,  c(50000,0,0,0))
data<-cbind(bedData,unlist(t(lapply(genes, function(x) {if(identical(x,character(0))){"None"} else{x}}))))
write.table(data,stdout(),col.names=FALSE,row.names=FALSE,quote=FALSE,sep="\t")

