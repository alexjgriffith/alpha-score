#!/data/binaries/R-3.1.0/bin/Rscript
library('getopt')
source("gene-assoc.r")

spec = matrix(c(
    'fileLocation','f', 1,"character"
    ),byrow=TRUE,ncol=4)
args=getopt(spec)
print("hello")
fileLocation="~/Dropbox/UTX-Alex/jan/combined_sorted.bed" #args$fileLocation 
bedData<-read.delim(fileLocation,header=0)
geneList<-read.delim("../info/hg19.RefSeqGenes.csv")
genes<-geneAssociation(bedData[1:100,],geneList,  c(50000,0,0,0))
for (i in genes) print(i)
data<-cbind(bedData[1:100,],unlist(t(lapply(genes, function(x) {if(identical(x,character(0))){"None"} else{x}}))))

write.table(data,stdout(),col.names=FALSE,row.names=FALSE,quote=FALSE,sep="\t")

