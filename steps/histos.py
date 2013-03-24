#import copy,array,os,collections
#import ROOT as r
from supy import analysisStep#,utils

#___________________________________________________________
class xyMap(analysisStep) :
    def __init__(self, coll='',indices='', index = None,nX=500,xLo=-5000.0,xHi=+5000.0,nY=500,yLo=-5000.0,yHi=+5000.0,title='') :
        for item in ['coll','indices','index','nX','xLo','xHi','nY','yLo','yHi','title'] : setattr(self,item,eval(item))
        self.moreName = coll + ("[i[%d]]:%s"%(index,indices) if index!=None else "")
        self.title = "%s;x [cm]; y [cm]"%(title if title else coll + ("[%s%s]"%(indices, "[%d]"%index if index!=None else "") if indices else ""))
    def uponAcceptance(self,eventVars) :
        positions = eventVars[self.coll]
        if positions is None : return
        if not self.indices:
            for p in positions :
                self.book.fill((p.x(), p.y()),
                               "%s_xy"%self.coll,
                               (self.nX, self.nY), (self.xLo, self.yLo), (self.xHi, self.yHi),
                               title=self.title)
            return
        indices = eventVars[self.indices]
        if self.index!=None :
            if self.index<len(indices) :
                p = positions[indices[self.index]]
                self.book.fill((p.x(), p.y()),
                               "%s_xy"%self.coll,
                               (self.nX, self.nY), (self.xLo, self.yLo), (self.xHi, self.yHi),
                               title=self.title)
            return
        for i in indices :
            p = positions[indices[i]]
            self.book.fill((p.x(), p.y()),
                           "%s_xy"%self.coll,
                           (self.nX, self.nY), (self.xLo, self.yLo), (self.xHi, self.yHi),
                           title=self.title)
#___________________________________________________________
