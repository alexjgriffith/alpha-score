#!/usr/bin/env python2.7
#
# This file is part of peakAnalysis, http://github.com/alexjgriffith/peaks/, 
# and is Copyright (C) University of Ottawa, 2014. It is Licensed under 
# the three-clause BSD License; see doc/LICENSE.txt.
# Contact: griffitaj@gmail.com
#
# Created : AU1862014
# File    : peak_functions
# Author  : Alexander Griffith
# Lab     : Dr. Brand and Dr. Perkins

import sys
import numpy as np
import matplotlib.pyplot as plt
import random
import time
from strToListClass import strToList

def parseInputList(string):
    options={"newList":"[" ,"closeList":"]" ,"setState":",","skipChar":["\""," "]}
    return (strToList(options))(string)

def loadLines(fi):
    seqs={}
    f=open(fi,"r")
    for line in f:
        if "#" not in line:
            a=line.strip().split("\t")
            if len(a)<2:
                print a
            if len(a)>2:
                temp=""
                seqs[a[0]]=parseInputList(temp.join(a[1::]))
            else:
                seqs[a[0]]=parseInputList(a[1])
    return seqs

def buildLines(lines):
    rets={}
    for i in lines:
        temp=[]
        for j in lines[i]:
            if j in lines:
                temp.append( lines[j])
            else:
                temp.append(j)
        rets[i]=temp
    return rets

def getCombos(contexts,context):
    combinations=[]
    for i in contexts[context]:
        if len(combinations)==0:
            combinations.append([i])
        else:
            templ=[]
            for j in combinations:
                templ.append(j+[i])
            combinations.extend(templ)
            combinations.append([i])
    return combinations

def cdf(temp,cats,context,combinations,start,end,step):
    #combinations=getCombos(cats,context)
    comboHash={}
    for i in combinations:
        comboHash[str(i)]=[]
    comboHash["width"]=[]
    width=start
    initLen=len(temp.data)
    while(True):
        start=time.time()
        temp.overlap(width)
        tlen=max([len(i.data) for i in temp.data])
        if width>end:
            break
        if width % 10 == 0:
          sys.stderr.write(str( width)+"\n")
        for combo in combinations:
            test=0
            for i in temp.data:
                if all([j in i.define.data[context]for j in combo ]):
                    if len(i.data)>1:
                        for k in i.data:
                            if k.define[context][0]==combo[0]:
                                test+=1                
            comboHash[str(combo)].append(test)
        comboHash["width"].append(width)
        width+=step
    return comboHash

def accessDirectory(fileName,string):
  # Replaces peak_processing.directory
  f= open(fileName,'r')
  for line in f:
    if "#" in line:
      continue
    a=(line.strip().split('\t'))
    if a[0]==string:
      return a[1]
  exit("there is no "+string+" in "+fileName+".")

class chooseLogFile():
    def __init__(self,logFile):
        self.storedStream=False
        if logFile=="stderr":
            self.f=sys.stderr
        elif logFile=="stdout":
            self.f=sys.stdout
        else:
            self.f=open(str(logFile),"w")
            self.storedStream=True
    def __call__(self):
        return self.f
    def write(self,output):
        self.f.write(output)
    def close(self):
        if self.storedStream:
            self.f.close()
        


class verboseOutput():
  """
  =Class verboseOutput()
  Logging function used in peakProcessing. Creates a closure
  based on wether or not the log is required. If the log
  is regected it passes all arguments.
  Args:
    verbose (bool): Sets the state of the closure to either
      print the response or pass.
    logFile (str,optional): Determines where the messages
     are logged to.
     options:
       * ``stderr``
       * ``stdout``
       *  filename
     The default is ``stderr``.
    tag (str,optional): Value to be placed in front of 
      every message. It can be any string. It is recomended 
      that the string end in " " or similar to allow for 
      basic parsing.By default tag is ""
  Returns:
    function: Retuns a logging if verbose is true
      otherwise it returns lambda : pass.
    file or None: If verbose is true then it returns
      the stream used for logging. Otherwise it returns
      None.
  Examples:
    case 1:
     >>> [test,testStream ]=verboseOutput(False).call()
     >>> test("print if verbose")
    case 2:          
     >>> [test,testStream ]=verboseOutput(True).call()
     >>> test("print if verbose")
      print if verbose
    case 3:
     >>> [test,testStream ]=verboseOutput(True).call()
     >>> test(["print if verbose",1,2,3])
     print if verbose 1 2 3
    case 4:
     >>> [test,testStream ]=
           verboseOutput(True,tag="verbose> ").call()
     >>> test("print if verbose")
     verbose> print if verbose 
    case 5:
     >>> [test,testStream ]=
           verboseOutput(True,logFile=test.log).call()
     >>> test("print if verbose")
     >>> testStream.close()
     shell > cat test.log
     shell > print if verbose
  """
  def __init__(self,verbose,logFile="stderr",tag="",sep=" "):
    if not verbose:
      self.fun=lambda x : ()
      self.f=None
    else:
      self.sep=sep
      self.tag=tag
      self.fun=self.caseTrue
      self.f=chooseLogFile(logFile)
      # Function self.output() of Class verboseOutput() 
      # is used in order to abstract the three posible 
      # logFile options.
      self.output=lambda message :self.f.write(message)

  def call(self):
    """
    -Function call() of Class verboseOutput()
    Call is used to return the function selected durring
    __init__. If modifications are nescisary of the
    verboseOutput object generated assign the object to a
    variable. If no modifications are nessisary call 
    ``verboseOutput(verbose).call()`` this will return the
    approriate function to be used.
    """
    return [self.fun,self.f]
      
  def caseTrue(self,message):
    """
    -Function caseTrue of Class verboseOutput()
    caseTrue is returned by call if verbose is not ``False``.
    caseTrue is the active method used to generate log files.
    Args:
      message (str,lsit): This is the string which will be printed
        to the log file. message can be a string or list. Note 
        that ``str(message)`` is called before printing so 
        message does not have to be a str.
    """
    self.output(str(self.tag))
    if isinstance(message,(list,tuple)):
      for i in message:
        self.output(str(i)+self.sep)
    else:
      self.output(str(message+self.sep))
    self.output("\n")


def large_scatter_plot_2(peaks_data, a_name,b_name,title=''):
  array=[]
  for key in peaks_data.joint_peaks:
    a=key.contexts["reads"][a_name]/(key.end -key.start)
    b=key.contexts["reads"][b_name]/(key.end -key.start)
    if a< 300 and  b<300 :
      array.append([ a,b])
  array=np.array(array).T
  order= array[0,:].argsort()
  data= array[0:2].T[order]
  a=data
  b = a.T[0] + a.T[1]*1.0j
  print b
  plt.close('all')
  data = data[np.unique(b,return_index=True)[1]]
  plt.plot(data.T[0], data.T[1], 'o')
  plt.title(title)
  plt.xlabel(a_name)
  plt.ylabel(b_name)
  #plt.show()
  plt.savefig("ppc"+str(a_name)+"_"+str(b_name))
  
def loadPeakFile(file_n,root=""):
  comment="#"
  filename=root+file_n
  peak_data=[]
  f= open(filename,'r')
  for line in f:
        if "#" in line:
          continue
        if line=="":
          continue
        a=(line.strip().split('\t'))
        filename=a[0]
        context={}
        i=1
        while i<len(a)-1:
            context[a[i]]=a[i+1]
            i+=2
        peak_data.append((filename,context))
  return peak_data

def buffer_assossiation(input_peaks):
    buffer_1=[]
    k=0
    #context="overlap"
    #catagories=["True","False"]
    for i in input_peaks:
      #i.addContext(context,catagories)
      #i.defining(context, None)
      buffer_2=[]
      start=int(i.start)
      end=int(i.end)
      chro=i.chro_order
      buffer_2.append(i)
      if len(buffer_1)>0:
        for j in buffer_1:
          if j.chro_order == chro:
            if int(j.end)>start:
              buffer_2.append(j)
      del buffer_1
      buffer_1=[]
      buffer_1=buffer_2
      del buffer_2
      if len(buffer_1) >1:
        k+=1
      """context magic"""
      for j in buffer_1:
        #if len(buffer_1)>1:
        #  value=1
        #  j.assignCatagoryValue( "overlap", "True",value)
        for x in buffer_1:
          value=abs(j.start-x.start)
          for m in x.define.keys():
            if  x.define[m]:
              comp=j.contexts[m][x.define[m][0]]
              fun=lambda x,y: ( x in y)
              if comp==None:
                j.assignCatagoryValue( m,x.define[m][0],value)
              else:
                j.assignCatagoryValue( m,x.define[m][0],value,comp,fun,comp)

def loadContextFile(filename):
    """
    May cause problems becouse it used to be a class
    """
    contexts={}
    comment="#"
    f= open(filename,'r')
    for line in f:
        catagories={}
        if "#" in line:
          continue
        a=(line.strip().split('\t'))
        tempCat={}
        cont=a[::-1].pop()
        for cat in a[1:]:
            tempCat[cat]=None
        contexts[cont]=tempCat.keys()
    return contexts

def loadChromosomeFile(filename):
    chromosomes=[]
    comment="#"
    f= open(filename,'r')
    for line in f:
        if "#" in line:
          continue
        chromosomes.append(line.strip().split('\t')[0])
    return chromosomes

def sortedMerge(peaks,temp):
    peaks_2=[]
    k=0
    n=0
    while True:
      #print k,n
      if k>=len(peaks):
        for i in temp[n:]:
          peaks_2.append(i)
        break
      if n>=len(temp):
        for i in peaks[k:]:
          peaks_2.append(i)
        break
      if temp[n].chro_order==peaks[k].chro_order:
        if temp[n].start<peaks[k].start:
            peaks_2.append(temp[n])
            n+=1
            continue
        elif temp[n].start>peaks[k].start:
            peaks_2.append(peaks[k])
            k+=1
            continue
        elif temp[n].start==peaks[k].start:
          peaks_2.append(peaks[k])
          peaks_2.append(temp[n])
          n+=1
          k+=1
          continue
      elif temp[n].chro_order<peaks[k].chro_order:
          peaks_2.append(temp[n])
          n+=1
          continue
      elif temp[n].chro_order>peaks[k].chro_order:
          peaks_2.append(peaks[k])
          k+=1
          continue
    return peaks_2
