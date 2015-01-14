#!/usr/bin/env python2.7
#
# This file is part of peakAnalysis, http://github.com/alexjgriffith/peaks/, 
# and is Copyright (C) University of Ottawa, 2014. It is Licensed under 
# the three-clause BSD License; see doc/LICENSE.txt.
# Contact: griffitaj@gmail.com
#
# Created : AUG262014
# File    : peakClass
# Author  : Alexander Griffith
# Lab     : Dr. Brand and Dr. Perkins

import sys
import os
import numpy
from peak_functions import *
from defineClass import define
from peakProcessingClass import peakProcessing
from UserList import UserList

class peakCapHandler(UserList):
    def __init__(self):
        self.data=[]
        self.blocked=[]
        self.blockedType=[]
        self.overlapValue=[]
    def add(self,peaks):
        for i in peaks:
            self.data.append(peakCap(i))
    def checkSort(self):
        for i in range(len(self.data)-1):
            if self.data[i].chro==self.data[i+1].chro:
                if self.data[i].max()>self.data[i+1].min():
                    print "value",i
                    return 1
            elif self.data[i].chro>self.data[i+1].chro:
                print "value chro",i,self.data[i].chro,self.data[i+1].chro
                return 1
        return 0
                                
    def merge(self,dataA,dataB):
        temp=dataA.data+dataB.data
        return peakCap(temp)

    def split(self,data,distance):
        buffer=[data.data[0]]
        splitPeaks=[]
        for i in range(len(data.data)-1):
            if data.data[i+1].summit-data.data[i].summit<distance:
                buffer.append(data.data[i+1])
            else:
                splitPeaks.append(peakCap(buffer))
                buffer=[data.data[i+1]]
        splitPeaks.append(peakCap(buffer))
        return splitPeaks

    def overlap(self,limit):
        self.overlapValue=limit
        ran=float(limit)
        temp=[self.data[0]]
        k=0
        peakA=temp[0]
        for i in range(len(self.data)-1):            
            peakB=self.data[i+1]
            if peakA.maxDiff()>=ran:
                t=self.split(peakA,ran)
                k+=len(t)-1
                temp.pop()
                temp.extend(t)
                peakA=temp[k]
            if peakA.chro==peakB.chro and peakB.min()-peakA.max()<ran:
                temp[k]=(self.merge(peakA,peakB))
                peakA=temp[k]
            else:
                temp.append(peakB)
                k=k+1
                peakA=temp[k]
        if peakA.maxDiff()>=ran:
            t=self.split(peakA,ran)
            temp.pop()
            temp.extend(t)
        self.data=temp
        

class peakCap():
    def __init__(self,data=None):
        self.data=[]
        self.summit=None
        self.define=define()
        self.maxum=0
        self.callSummit=lambda : [i.summit for i in self.data]
        if isinstance(data,list):
                for i in data:
                    self.define.add(i.define.data)
                    self.chro=i.chroOrder
                    self.data.append(i)
                self.maxum=self.maxDiff()
        else:
            self.define.add(data.define.data)
            self.chro=data.chroOrder
            self.data.append(data)
            self.maxum=0
        self.summit=np.mean(self.callSummit())
        
    def maxDiff(self):
        if self.maxum==0:
            temp=0
            for i in range(len(self.data)-1):
                if self.data[i+1].summit-self.data[i].summit>temp:
                    temp=self.data[i+1].summit-self.data[i].summit
            self.maxum=temp
            return temp
        else:
            return self.maxum
    def max(self):
        return max(self.callSummit())
    def min(self):
        return min(self.callSummit())

class peak():
    def __init__(self,chro,summit,defines):
        self.chro=chro
        self.summit=summit
        self.score=0
        self.define=define()
        self.define.add(defines)
    def addScore(self,score):
        self.score=float(score)
    def buildChroOrder(self,chromosomeList):
        self.chroOrder= np.where([self.chro==i for i in chromosomeList])[0].astype('int')[0]
    def __call__(self):
        return self.chro,self.summit
