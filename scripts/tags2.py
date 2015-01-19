import sys
from numpy import mean,std

class peak():
    def __init__(self,args):
        chrom,start,end,fasta,score =args
        self.chrom=chrom
        self.start=int(start)
        self.end=int(end)
        self.fasta=fasta[0:-1]
        self.score=float(score)
        
def printPeaks(peakList):
    for peak in peakList:
        outString=">"+peak.chrom+":"+str(peak.start)+"-"+str(peak.end)+"\n"+peak.fasta+"\n"
        sys.stdout.write(outString)
        
def main():
    filename=file(sys.argv[1])
    a=0
    peaks=[]
    for line in filename:
        if not("#" in line):
            peaks.append(peak([line.strip().split()[i] for i in [0,1,2,3,4]]))
    x=[i.score for i in peaks]
    n=1
    s=std(x)
    m=mean(x)
    top= lambda x : [i for i in x if i.score > s*n+m]
    notTop= lambda x : [i for i in x if i.score < s*n+m]
    bottom=lambda x :[i for i in x if i.score < m-s*n]
    notBottom=lambda x :[i for i in x if i.score > m-s*n]
    middle=lambda x :[i for i in x if i.score > m-s and  i.score < m+s]
    option={"top":top,"bottom":bottom,"middle":middle,"notTop":notTop,"notBottom":notBottom}
    printPeaks(option[sys.argv[2]](peaks))
        

if __name__=='__main__':
    main()
