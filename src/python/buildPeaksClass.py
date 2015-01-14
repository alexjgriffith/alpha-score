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

"""
Notes:
  this stems from the now defunced peak_source.py file
  the peak_processing class has been wrapped in builPeaks
  this makes the workspace esier to set up.
  peakProcessing unlike peak_processing is based on a 
  list structure, you can pass around the object and 
  treat it like a modified list.

  merge filter functions in workspace
  provide filtering exaples for ease of use

  The seperation of buildPeaks,peakProcessing, and peaks
  allows for easier analysis of each function
"""

import sys
import numpy
from peak_functions import *
from peakBaseClass import peakBase
from peakClass import peak,peakCap,peakCapHandler
from defineClass import define

class buildPeaks():
    """"
    This class is responsible for building and adding to peak
    data lists.
    """
    def __init__(self,settingsFile,trip=True,chromosomeLoc=None):
        self.chromosomeLoc=chromosomeLoc
        self.settings=settingsFile
        self.data=[]
        if (trip):
            self.loadFiles()
        else:
            if (self.chromosomeLoc):
                self.loadSingleFile()
            else:
                exit("need to provide a chromosome location")

    def loadSingleFile(self):
        self.peakFileList=loadPeakFile(self.settings)   
        self.chromosomeList=loadChromosomeFile(self.chromosomeLoc)
        pos=range(2,len(self.peakFileList[0]),2)
        contextValues=self.peakFileList[0][1].keys()
        contexts={}
        for i in self.peakFileList:
            for l,j in zip(pos,contextValues):
                try:
                    contexts[j].append(i[l+1])
                except:
                    contexts[j]=[i[l+1]]
        self.contexts={}
        for  i in contexts.keys():
            self.contexts[i]=list(set(contexts[i]))
        for peakFile in self.peakFileList:
            self.data=self.data+self.unwrap(peakFile,self.contexts,di="")
        self.data.sort(key= lambda x : (x.chroOrder,x.summit))

    def loadFiles(self):
        """
        Added to remove code duplication
        """
        self.peakFileList=loadPeakFile(accessDirectory(self.settings,"peakFile")) 
        self.contexts=loadContextFile(accessDirectory(self.settings,"contextFile"))
        self.chromosomeList=loadChromosomeFile(accessDirectory(self.settings,"chromosomeFile"))
        for peakFile in self.peakFileList:
            self.data=self.data+self.unwrap(peakFile,self.contexts)
        self.data.sort(key= lambda x : (x.chroOrder,x.summit))

    def __call__(self,version='all',settingsFile=None,block=None):
        if not settingsFile==None:
            self.data=[]
            self.settings=settingsFile
            self.loadFiles()
        return self.data

    def unwrap(self,i,contexts,di=False):
        (file_name,cont)=i
        if (di==False):
            if accessDirectory(self.settings,"peaks"):
                di=accessDirectory(self.settings,"peaks")
            else:
                exit("couldn't find peaks:\t"+self.settings)
        temp=self.importPeaks(str(di)+str(file_name),cont)
        return temp

    def importPeaks(self,input_file,cont):
        peakList=[]
        f= open(input_file,'r')
        for line in f:
                a=(line.strip().split('\t'))
                if a[0] in self.chromosomeList:
                    temp=peak(a[0],int(a[1]),cont)
                    temp.addScore(a[2])
                    temp.buildChroOrder(self.chromosomeList)
                    peakList.append(temp)                    
        return peakList


