#import copy,array,os,collections
#import ROOT as r
from supy import analysisStep, steps#,utils
from math import pi

#___________________________________________________________
class rho(steps.histos.value) :
    def wrapName(self) : return ".rho"
    def wrap(self,val) : return val.rho()
#___________________________________________________________
class eta(steps.histos.value) :
    def wrapName(self) : return ".eta"
    def wrap(self,val) : return val.eta()
#___________________________________________________________
class value2d(analysisStep) :
    def __init__(self, var=('',''),
                 indices='', index = None,
                 N=(100,100),lo=(0.0,0.0),hi=(1.0,1.0),title='',w=None) :
        for item in ['var','indices','index','N','lo','hi','title','w'] : setattr(self,item,eval(item))
        self.moreName = '_vs_'.join([var[1]+self.wrapNameY(), var[0]+self.wrapNameX()]) \
            + (":%s"%indices if indices and index==None else "") \
            + ("[i[%d]]:%s"%(index,indices) if index!=None else "")
        self.title = "%s;%s;%s" % (title if title else \
                                       ' vs '.join([self.wrapNameY(), self.wrapNameX()]) \
                                       + ("[%s]"%indices if indices and index==None else "") \
                                       + ("[%s[%d]]"%(indices,index) if indices and index!=None else ""),
                                   var[0] + self.wrapNameX(),
                                   var[1] + self.wrapNameY())

    def uponAcceptance(self,eventVars) :
        valX, valY = eventVars[self.var[0]], eventVars[self.var[1]]
        if valX is None or valY is None : return
        if not self.indices:
            self.book.fill((self.wrapX(valX), self.wrapY(valY)),
                           self.moreName,
                           self.N, self.lo, self.hi, title = self.title,
                           w = (eventVars[self.w] if self.w else None))
            return
        indices = eventVars[self.indices]
        if self.index!=None :
            if self.index<len(indices) :
                self.book.fill((self.wrapX(valX[indices[self.index]]), self.wrapY(valY[indices[self.index]])),
                               self.moreName,
                               self.N, self.lo, self.hi, title = self.title,
                               w = (eventVars[self.w] if self.w else None))
            return
        for i in indices :
            self.book.fill((self.wrapX(valX[i]), self.wrapY(valY[i])),
                           self.moreName,
                           self.N, self.lo, self.hi, title = self.title,
                           w = (eventVars[self.w] if self.w else None))
    def wrapNameX(self) : return ''
    def wrapNameY(self) : return ''
    def wrapX(self, val) : return val
    def wrapY(self, val) : return val
#___________________________________________________________
class yVsX(value2d):
    def __init__(self, var=('',''), indices='', index = None, N=(500,500),lo=(-5000.0,-5000.0),hi=(+5000.0,+5000.0),title='',w=None) :
        super(yVsX, self).__init__(var, indices, index, N, lo, hi, title, w)

    def wrapNameX(self) : return '.x'
    def wrapNameY(self) : return '.y'
    def wrapX(self, val) : return val.x()
    def wrapY(self, val) : return val.y()
#___________________________________________________________
class phiVsEta(value2d):
    def __init__(self, var=('',''), indices='', index = None, N=(100,100),lo=(+1.0,-pi),hi=(+3.0,+pi),title='',w=None) :
        super(phiVsEta, self).__init__(var, indices, index, N, lo, hi, title, w)
    def wrapNameX(self) : return '.eta'
    def wrapNameY(self) : return '.phi'
    def wrapX(self, val) : return val.eta()
    def wrapY(self, val) : return val.phi()
#___________________________________________________________
class phiVsTheta(value2d):
    def wrapNameX(self) : return '.theta'
    def wrapNameY(self) : return '.phi'
    def wrapX(self, val) : return val.theta()
    def wrapY(self, val) : return val.phi()
