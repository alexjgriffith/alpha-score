
# addContext
# assignCatagoryValue
# defining


# a cNode can be a dict , list or None
# need a builder function
# Design a complete context structure and the methods to
# Handle it
# the buffermerge needs to be split into portions, append
# in the cnode object can replace initial assignment portion

#
#
#

class cNode(object):
    def __init__ (self,contexts=None,catagories=None):
        self.contexts={}
        if contexts!= None and catagories != None and len(contexts)==len(b):
            self.append(contexts,catagories)
    def append (self,contexts,catagories):
        for cont in contexts:
            tempCat={}
            catList=catagories[tempCat]
            for cat,nil in zip(catList,[None for j in range(len(catList))]):
                tempCat[cat]=nil
            self.contexts[cont]=tempCat        
    def __call__(self):
        return self.contexts
    def assignCatagoryValue(self, context, catagory,value,comp=None,fun=lambda x,y: x!=y , alt=None):
        if self.checkCatagory(context,catagory):
            if fun(value,comp):
                if isinstance(self.contexts[context][catagory],(list)):
                    self.contexts[context][catagory].append(value)
                else:
                    self.contexts[context][catagory]=[value]
            else:
                self.contexts[context][catagory]=[alt]
    def checkCatagory(self,context,catagory):
        if context in self.contexts.keys():
            if catagory in self.contexts[context].keys():
                return 1
        return 0

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
        cat=a[1:]
        for cat in a:
            tempCat[cat]=None
        contexts[cont]=tempCat
    return contexts



        for cont in contexts:
            tempCat={}
            catList=catagories[tempCat]
            for cat,nil in zip(catList,[None for j in range(len(catList))]):
                tempCat[cat]=nil
            self.contexts[cont]=tempCat        



filename="/home/agriffith/Masters/peaks/projects/august/settings/contexts2.load"
contexts=loadContextFile(filename)

f=open(filename,'r')
contextList
a=["type","name"]
b=[["A","B"],["temp","park"]]
temp=cNode(a,b)
temp.checkCatagory("temp","A")
temp.checkCatagory("type","A")
temp.assignCatagoryValue("type","A",1)
temp()
