#!/usr/bin/env R
#
# This file is part of peakAnalysis, http://github.com/alexjgriffith/alpha-score/, 
# and is Copyright (C) University of Ottawa, 2015. It is Licensed under 
# the three-clause BSD License; see LICENSE.txt.
# Contact: griffitaj@gmail.com

buildAnotations<-function(...){
    value<-c(...)
    l=length(value)
    br=""
    if(modulous(l,2)==0)
        collect(seq(from=1,to=l,by=2),function(x){collapse(" ",value[x],'="',value[x+1],'"')})}
        
htmlTags<-function(tag,value=FALSE,anotations=FALSE){
    closeT<-"/>"
    an<-""
    if(FALSE != anotations[1])
        an<-lcollapse(anotations)
    if(FALSE != value)
        closeT<-collapse(an,">",value,"</",tag,">")
    else
        closeT<-collapse(an,closeT)
    collapse("<",tag,closeT)}

htmlDoc<-function(...,doctype="<!DOCTYPE html>",tag="html"){
    html<-htmlTags(tag,collapse(...))
    collapse(doctype,html)}

htmlTable<-function(x,...){
    br<-""
    shape<-dim(x)
    for(i in seq(shape[1]))
        {
            tr<-""
        for(j in seq(shape[2]))
            tr<-collapse(tr,htmlTags("td",x[i,j]))
            br<-collapse(br,htmlTags("tr",tr))
         }   
    htmlTags("table",br,...)}

htmlImage<-function(location,...){
    htmlTags("img",anotations=c(buildAnotations("src",location)),...)}

