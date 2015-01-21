import sys
from numpy import mean,std,matrix,argsort,sort,fft
import tags2
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

import colorsys

def get_N_HexCol(N=5):

    HSV_tuples = [(x*1.0/N, 0.5, 0.5) for x in xrange(N)]
    hex_out = []
    for rgb in HSV_tuples:
        rgb = map(lambda x: int(x*255),colorsys.hsv_to_rgb(*rgb))
        hex_out.append("".join(map(lambda x: chr(x).encode('hex'),rgb)))
    return hex_out

def main():
    fileLocation=sys.argv[1]
    seperationFunction=sys.argv[2]
    cutOff=sys.argv[3]
    filename=file(fileLocation)
    lada=tags2.loadPeaks(filename)

    peaks=tags2.builderSplit(lada,n=float(cutOff))
    classes=set()
    for i in lada:
        i.fasta=i.fasta.split("-")
        a=set(i.fasta)
        classes=a.union(classes)
    classes=list(classes)
    data=peaks(seperationFunction)
    printData(data,lada,classes)
    #prat=buildHistogram(data,["jurk","eryt","meka","rpmi","k562"],normalize=True)
    #plotStackedPDF(prat,["jurk","eryt","meka","rpmi","k562"])

def buildHistogram(data,classes,n=100,normalize=False):
    m=min([i.score for i in data])
    M=max([i.score for i in data])
    step=(M-m)/n
    da={}
    for j in classes:
        da[j]=0.0
    prat=[(da,0)]
    p=0
    for i in range(n):
        da={}
        for k in classes:
            da[k]=0
        lim=step*float(i)+m
        lim2=step*float(i+1)+m
        temp=[j for j in data if j.score > lim and j.score < lim2]
        tot=0
        for k in temp:
            for j in k.fasta:
                if j in classes:
                    da[j]+=1.0
                    tot+=1.0
        if(normalize==False): 
            tot=1
        if (tot!=0):
            for j in classes:
                da[j]=da[j]/tot
        else:
            da=prat[p][0]
        p+=1
        prat.append((da,step*i+m))
    prat=prat[1:]
    return prat

def plotPDFs(prat,classes):
    x=[i[1] for i in prat]
    for names in classes:
        temp=[i[0][names] for i in prat]
        tert=[0]
        for i in range(len(temp)):
            tert.append(tert[i]+temp[i])
        print len(tert), len(x),tert[-1]
        temp2=[j/tert[-1] for j in temp]
        plt.plot(x,temp)
    plt.show()
    exit()

def plotStackedPDF(prat,classes):
    x=[i[1] for i in prat]
    print x[0:2]
    n=len(prat)
    N=len(classes)
    pData=[[prat[i][0][j] for i in range(n)] for j in classes ]
    order=argsort([sum(i) for i in pData])
    pData=[ pData[i] for i in order]    
    cols = [[colorsys.hsv_to_rgb(k*1.0/N,0.5, 0.5) for k in xrange(N)][i] for i in order]
    for i in [j+1 for j in range(N-1)]:
        temp=[k+j for k,j in zip(pData[i],pData[i-1])]
        pData[i]=temp
    i=0
    plt.plot(0, 0,color=cols[0],label=classes[order[i]],linewidth=10)
    plt.fill_between(x, pData[0], 0,color=cols[0])
    for i in [j + 1 for j in range(N-1)]:
        plt.plot(0,0,color=cols[i],label=classes[order[i]],linewidth=10)
        plt.fill_between(x, pData[i], pData[i-1],color=cols[i])
    plt.legend()
    plt.xlabel("PCA Value")
    plt.ylabel("Number of Peaks")
    plt.title("PC1 mean-sd*6<x<mean+sd*6")
    plt.show()

def printData(data,lada,classes):
    for i in classes:
        sys.stdout.write( str(i)+"\t"+
                          str(100*float(len([j.fasta for j in data if i in j.fasta]))/float(len(data)))[0:4]+"%"+"\t"+
                          str(100*float(len([j.fasta for j in data if i in j.fasta]))/float(len([n.fasta for n in lada if i in n.fasta])))[0:4]+"%"
                          +"\t"+str(len([j.fasta for j in data if i in j.fasta and len(j.fasta)==1]))+"\t"+str(len([j.fasta for j in data if i in j.fasta]))+"\n")
        #print(i,float(len([j.fasta for j in data if i in j.fasta]))/float(len([n.fasta for n in lada if i in n.fasta])))
    print(len(data))


if __name__=='__main__':
    main()

