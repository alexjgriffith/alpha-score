#!/usr/bin/env python2.7
#
# This file is part of peakAnalysis, http://github.com/alexjgriffith/peaks/, 
# and is Copyright (C) University of Ottawa, 2014. It is Licensed under 
# the three-clause BSD License; see doc/LICENSE.txt.
# Contact: griffitaj@gmail.com
#
# Created : AUG262014
# File    : buildPeaksClass
# Author  : Alexander Griffith
# Lab     : Dr. Brand and Dr. Perkins

import sys
from numpy import mean,std

class peak():
    def __init__(self,args):
        chrom,start,end,fasta,score =args
        self.chrom=chrom
        self.start=int(start)
        self.end=int(end)
        self.fasta=fasta
        self.score=float(score)
        
def printFasta(peakList):
    for peak in peakList:
        outString=">"+peak.chrom+":"+str(peak.start)+"-"+str(peak.end)+"\n"+peak.fasta[0:-1]+"\n"
        sys.stdout.write(outString)

def printInfo(peakList):
    for peak in peakList:
        outString=peak.fasta+"\n"
        sys.stdout.write(outString)

def loadPeaks(filename):
    a=0
    peaks=[]
    for line in filename:
        if not("#" in line):
            peaks.append(peak([line.strip().split()[i] for i in [0,1,2,3,4]]))
    return(peaks)
        
class builderSplit():
    top= lambda self,x,n,m,s : [i for i in x if i.score > s*n+m]
    notTop= lambda self,x,n,m,s : [i for i in x if i.score < s*n+m]
    bottom=lambda self,x ,n,m,s:[i for i in x if i.score < m-s*n]
    notBottom=lambda self,x,n,m,s :[i for i in x if i.score > m-s*n]
    middle=lambda self,x,n,m,s :[i for i in x if i.score > m-s*n and  i.score < m+s*n]
    all=lambda self,x,n,m,s :x
    def __init__(self,peaks,n=1,options=None):
        self.peaks=peaks
        x=[i.score for i in peaks]
        self.n=n
        self.s=std(x)
        self.m=mean(x)
        if options==None:
            self.option={"top":self.top,"bottom":self.bottom,"middle":self.middle,"notTop":self.notTop,"notBottom":self.notBottom,"all":self.all}
        else:
            self.option=options
    def __call__(self,value):
        return self.option[value](self.peaks,self.n,self.m,self.s)
        
def main():
    filename=file(sys.argv[1])
    peaks=builderSplit(loadPeaks(filename),n=float(sys.argv[3]))
    if(sys.argv[3]=="info"):
        printInfo(peaks(sys.argv[2]))
    elif(sys.argv[3]=="fasta"):
        printFasta(peaks(sys.argv[2]))
    else:
        peaks(sys.argv[2])
        

if __name__=='__main__':
    main()
