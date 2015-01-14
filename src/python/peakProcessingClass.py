#!/usr/bin/env python2.7
#
# This file is part of peakAnalysis, http://github.com/alexjgriffith/peaks/, 
# and is Copyright (C) University of Ottawa, 2014. It is Licensed under 
# the three-clause BSD License; see doc/LICENSE.txt.
# Contact: griffitaj@gmail.com
#
# Created : AUG262014
# File    : peakProcessingClass
# Author  : Alexander Griffith
# Lab     : Dr. Brand and Dr. Perkins

import sys
import numpy
import UserList
from peak_functions import *
from defineClass import define



class peakProcessing():
    def displayRegionContribution(self,context,cross,filename="stderr",tag=""):
        data={}
        relation={"stem": ["cd34","cd133","meka","ecfc"],
                  "normal": ["k562","eryt"],
                  "abnormal": ["jurk","cem","rpmi","tall_p1","tall_p2","tall_p3"]}
        temp=self.getContextOverlap(context)
        for k in temp:
            data[k]={}
            ap=temp[k]
            if len(ap)>0:
                sp=self.getUniquePeaks(cross,data=ap,fun=lambda j: j>1)
                up=self.getUniquePeaks(cross,data=ap,fun=lambda j: j==1)
            else:
                sp={}
                up={}
            for i in up.keys():
                data[k][i]=[len(sp[i]),len(up[i])]
        outputList={}
        singleCase = lambda contexts,conts,j : [conts[0],"unique"]
        allCase = lambda contexts,cont,j : ["all"]
        def overlapCase(contexts,cont,j):
            for k in conts:
                if not j in contexts[k]:
                    return [k]
        options={1:singleCase,2:overlapCase,3:allCase}
        for i in data.keys():
            conts=i.split("-")
            for j in data[i].keys():
                con = options[len(conts)](relation,conts,j)
                for k in range(len(con)):
                    if not all(i==0 for i in data[i][j]):
                        try:
                            temp=con[k]
                            outputList[temp][j]=data[i][j][k]
                        except:
                            outputList[temp]={}
                            outputList[temp][j]=data[i][j][k]
        catagories=[]
        for i in relation.values():
            catagories.extend(i)
        contexts=["unique","abnormal","normal","stem","all"]
        sys.stdout.write("\t")
        for k in contexts:
            sys.stdout.write(str(k)+"\t")
        sys.stdout.write("\n")
        for i in catagories:
            sys.stdout.write(str(i)+"\t")
            for k in contexts:
                try:
                    sys.stdout.write(str(outputList[k][i])+"\t")
                except:
                    sys.stdout.write(str(0)+"\t")
            sys.stdout.write("\n")

    def getUniquePeaks(self,typ,data=None,fun=lambda j: j>1):
      """
      Tests to see if a peak is unique or not. By default
      it returns shared peaks. Passing it 

      fun= lambda j: j==1

      will make it return unique peaks.
      """
      if data==None:
          data=self.data
      uniquePeaks={}
      for i in data:
          for j in data.define[typ]:
              if not uniquePeaks[j]:
                  uniquePeaks[j]=[]
      for i in data:
        n=0
        if len(i.data)!=1:
            n+=1
        if fun(n): # if n>1: #<-By default
            for j in i.define[typ]:
                uniquePeaks[j].append(i)
      return uniquePeaks

    def getContextOverlap(self,catagory):
        states={}
        for i in self.data:
            a=""
            for n in i.define[catagory]:
                a+=n
                a+="-"
            a=a[:-1]
            try:
                states[a].append(i)
            except:
                states[a]=[i]
        return states
