#!/usr/bin/env python2.7
#
# This file is part of peakAnalysis, http://github.com/alexjgriffith/peaks/, 
# and is Copyright (C) University of Ottawa, 2014. It is Licensed under 
# the three-clause BSD License; see doc/LICENSE.txt.
# Contact: griffitaj@gmail.com
#
# Created : SEP42014
# File    : peakBuilder
# Author  : Alexander Griffith
# Lab     : Dr. Brand and Dr. Perkins

class define():
    def __init__(self):
        self.data={}
        self.contexts=[]
    def __getitem__(self,number):
        return self.data[number]
    def add(self,hashs):
        for context in hashs.keys():
            catagory = hashs[context]
            self.contexts.append(context)
            try:
                self.data[context]=list(set(self.data[context])|set(catagory))
            except:
                if isinstance(catagory,list):
                    self.data[context]=catagory
                else:
                    self.data[context]=[catagory]

