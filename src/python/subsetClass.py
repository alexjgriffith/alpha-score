#!/usr/bin/env python2.7
#
# This file is part of peakAnalysis, http://github.com/alexjgriffith/peaks/, 
# and is Copyright (C) University of Ottawa, 2014. It is Licensed under 
# the three-clause BSD License; see doc/LICENSE.txt.
# Contact: griffitaj@gmail.com
#
# Created : SEP262014
# File    : strToListClass
# Author  : Alexander Griffith
# Lab     : Dr. Brand and Dr. Perkins


#from peakClass import peakCapHandler
#from peak_functions import *

class subsetWraper():
    not1  = lambda self,lis: not(lis[0])
    ainter= lambda self,lis: all(lis)
    aunion= lambda self,lis: any(lis)
    def __init__(self,data,a,name):
        self.name=name
        self.k=[]
        self.output=None
        for i in range(len(data)):
            self.k.append(self.getSubset(a,data[i].define.data))        
    def __repr__(self,data=False,width=False):
        if self.output==None:
            return str(self.name)+str(self.count()) 
        else:
            a=""
            for i in self.output:
                a+=i[0]+"\t"+i[1]+"\t"+i[2]+"\n"
            return a

    def zeroTest(double,value):
        lower=double-value
        upper=double+value
        if lower<0:
            double=0
            upper=upper-lower
        return str(int(lower)),str(int(upper))

    def printablePeaksType(self,data):
        dataActive=[data.data[i] for i in self.order()]
        for i in  dataActive:
            temp=self.zeroTest(i.summit,width)
            self.output.append([str(i.data[0].chro),temp[0],temp[1]]) 

    def printablePeaks(self,data,width=False):
        self.output=[]
        if width==False:
            width=data.overlapValue
        dataActive=[data.data[i] for i in self.order()]
        for i in  dataActive:
            temp=self.zeroTest(i.summit,width)
            self.output.append([str(i.data[0].chro),temp[0],temp[1]]) 

    def count(self,value=True):
        return self.k.count(value)

    def order(self):
        return [i for i in range(len(self.k)) if self.k[i]==True]
            
    def analyze(self,data,values):
        context,catagories=values
        return catagories in data[context]

    def getSubset(self,a,data):
        k=[]
        for i in a[1::]:
            if isinstance(i,list):
                k.append(self.getSubset(i,data))
            if isinstance(i,str):            
                k.append(self.analyze(data,i.split(":")))
        return self.builder(a[0],k)

    def builder(self,fun,values):
        functions={'union':self.aunion,
                   'intersection':self.ainter,
                   'not':self.not1}
        return functions[fun](values)


