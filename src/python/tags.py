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
import numpy
import argparse
from peak_functions import *
from buildPeaksClass import buildPeaks
from peakClass import peak,peakCap,peakCapHandler
from defineClass import define
from subsetClass import subsetWraper

def fromStdin():
    parser=argparse.ArgumentParser(prog="TAG",description="Combine and tag input files.",epilog="File Format: <bed file location><catagory><value>...")
    parser.add_argument('-i','--in-file',dest='fileLocation')
    parser.add_argument('-c','--chromosome',dest='chromosomeLoc')
    parser.add_argument('-m','--macs',dest='MACS',action='store_true')
    parser.add_argument('-t','--tags',dest='TAGS',action='store_true')
    parser.add_argument('-s','--summits',dest='SUMMITS',action='store_true')
    return parser.parse_args(sys.argv[1:])

def zeroTest(double,value):
    lower=double-value
    upper=double+value-1
    if lower<0:
        double=0
        upper=upper-lower
    return str(int(lower)),str(int(upper))

def main():
    args=fromStdin()
    rawpeaks=(buildPeaks(args.fileLocation,trip=False,chromosomeLoc=args.chromosomeLoc))()
    peaks=peakCapHandler()
    peaks.add(rawpeaks)
    peaks.overlap(350)
    a=lambda i :i.data[0].chro
    b=lambda i :i.define.data["name"] 
    c=lambda i ,o :zeroTest(i.summit,o)
    d=lambda i : [str(j.score) for j in i.data]
    e=lambda i : [str(j.summit) for j in i.data]
    x=[[a(i),c(i,150),d(i),b(i),e(i)]  for i in peaks.data]
    for i in range(len(peaks.data)):
        sys.stdout.write( x[i][0]+"\t"+ str(x[i][1][0])+"\t"+ str(x[i][1][1])+"\t")
        if(args.MACS):
            sys.stdout.write("{")
            for j in range(len(x[i][2])-1):
                sys.stdout.write(str(x[i][3][j])+":"+str(x[i][2][j])+",")
            sys.stdout.write(str(x[i][3][-1])+":"+x[i][2][-1]+"}\t")
        if(args.SUMMITS):
            sys.stdout.write("{")
            for j in range(len(x[i][4])-1):
                sys.stdout.write(str(x[i][3][j])+":"+str(x[i][4][j])+",")
            sys.stdout.write(str(x[i][3][-1])+":"+x[i][4][-1]+"}\t")
        if(args.TAGS):
            for j in range(len(x[i][3])-1):
                sys.stdout.write(str(x[i][3][j])+"-")
            sys.stdout.write(x[i][3][-1])
        sys.stdout.write("\n")

if __name__=='__main__':
    main()
