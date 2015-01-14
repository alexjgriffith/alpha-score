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

class strToList :
    def __init__(self,options,saveState=False):
        #self.interest={"[":newList,"]":"closeList"}
         # allows for
        self.saveState=saveState
        ints=["newList","closeList","setState","skipChar"]
        posibs={"newList":self.newList ,"closeList":self.closeList ,"setState":self.setState,"skipChar":self.skipChar}
        self.posibs=options
        self.options={}
        for i in options.keys():
            if i in ints:
                if isinstance(options[i],list):
                    for k in options[i]:
                        self.options[k]=posibs[i]
                else:
                    self.options[options[i]]=posibs[i]
        #print self.options.keys()
        #self.options={"[":self.newList ,"]":self.closeList ,",":self.setState,"\"":self.skipChar}
        #print self.options.keys()

    def __call__(self,string,val=None):
        return self.parseBuilder(val,string)

    def setState(self,outList,string):
        if self.saveState==False:
            outList.append("")
        else:
            if not outList[-1]=="":
                outList.append("")
        return self.parseBuilder(outList,string[1::])

    def newList(self,outList,string):
        if isinstance(outList,list):
            temp=[]
            i=0
            depth=0
            for t in string:
                if t in self.posibs["newList"]:
                    depth+=1
                elif t in self.posibs["closeList"]:
                    depth-=1
                    if depth==0:
                        break
                i+=1
            if depth>0:
                exit("Unmatched Bracket")
            temp=self.parseBuilder(temp,string[1:i])
            if len(outList)>0: 
                if outList[-1]=="":
                    outList[-1]=temp
                else:
                    outList.append(temp)
            else:
                outList.append(temp)
            return self.parseBuilder(outList,string[i::])
        else:
            outList=[]
        return self.parseBuilder(outList,string[1::])
    
    def closeList(self,outList,string):
        return self.parseBuilder(outList,string[1::])

    def pushChar(self,outList,string):
        if len (outList)>0:
            outList[-1]+=string[0]
        else:
            outList.append(string[0])
        return self.parseBuilder(outList,string[1::])

    def skipChar(self,outList,string):
        return self.parseBuilder(outList,string[1::])

    def parseBuilder(self,outList,string):
        if len(string)==0:
            return outList
        if string[0] in self.options.keys():
            func=self.options[string[0]]
        else:
            func=self.pushChar
        return func(outList,string)
