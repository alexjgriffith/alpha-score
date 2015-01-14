import sys
import pylab as plt
sys.path.append("/mnt/brand01-00/mbrand_analysis/lib/matplotlib_venn/")
from venn3 import venn3, venn3_circles
from venn_util import venn3_unweighted, venn2_unweighted
import itertools
from  subsetClass import subsetWraper

class buildVennDiagram():
    def __init__(self,data):
        self.data=data

    def __call__(self,title,seqs,labels):
        if len(seqs)>3:
            return 0
        x=[]
        for i in range(len(seqs)):
            x.extend([i for i in itertools.combinations(seqs,i+1)])
        combs=[]
        for i in x:
            A=list(i)
            A.append("intersection")
            A=A[::-1]
            B=self.nots(i,seqs)
            if B:
                B.append("union")
                B=B[::-1]
                B=["not",B]
                A.append(B)
            temp=subsetWraper(self.data,A,i).count()
            combs.append([temp,str(i)])
        self.venn_build(title,[i[0]for i in combs],labels)

    def vennBuild(self,title,bis,labels):
        if len(bis)>3:
            v = venn3_unweighted(subsets=([bis[i] for i in [0,1,3,2,4,5,6]]),set_labels=(labels[0],labels[1],labels[2]))
            v.get_label_by_id('100').set_text(str(bis[2]))
            v.get_label_by_id('010').set_text(str(bis[1]))
            v.get_label_by_id('001').set_text(str(bis[0]))
        elif len(bis)==3:
            v = venn2_unweighted(subsets=(bis),set_labels=(labels[0],labels[1]))
            v.get_label_by_id('10').set_text(str(bis[0]))
            v.get_label_by_id('01').set_text(str(bis[1]))
        plt.title(title)
        plt.savefig(title+'venn.png')
        plt.close()

    def nots(self,val,seqs):
        return [i for i in seqs if not i in val]
