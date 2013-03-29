#import copy,array,os,collections
import ROOT as r
from supy import steps, analysisStep
from math import pi

#___________________________________________________________
class rho(steps.histos.value) :
    def wrapName(self) : return ".rho",
    def wrap(self,val) : return val[0].rho()
#___________________________________________________________
class eta(steps.histos.value) :
    def wrapName(self) : return ".eta",
    def wrap(self,val) : return val[0].eta()
#___________________________________________________________
class yVsX(steps.histos.value) :
    def __init__(self, var=('',''), indices='', index = None, N=(500,500),low=(-5000.0,-5000.0),up=(+5000.0,+5000.0),title='',w=None) :
        super(yVsX, self).__init__(var, N, low, up,  indices, index, title, w)

    def wrapName(self) : return ('.x', '.y')
    def wrap(self, val) : return (val[0].x(), val[1].y())
#___________________________________________________________
class phiVsEta(steps.histos.value):
    def __init__(self, var=('',''), indices='', index = None, N=(100,100),lo=(+1.0,-pi),hi=(+3.0,+pi),title='',w=None) :
        super(phiVsEta, self).__init__(var, N, lo, hi, indices, index, title, w)
    def wrapName(self) : return ('.eta', '.phi')
    def wrap(self, val) : return (val[0].eta(), val[1].phi())
#___________________________________________________________
class phiVsTheta(steps.histos.value):
    def __init__(self, var=('',''), indices='', index = None, N=(100,100),lo=(+0.10,-pi),hi=(+0.75,+pi),title='',w=None) :
        super(phiVsTheta, self).__init__(var, N, lo, hi, indices, index, title, w)
    def wrapName(self) : return ('.theta', '.phi')
    def wrap(self, val) : return (val[0].theta(), val[1].phi())
#___________________________________________________________
class padIndexAvg(analysisStep) :
    "Plot the pad index average(ieta or iphi)"
    def __init__(self, coll, indices='', ieta=False, iphi=False,
                 N=(100,100),lo=(-5000.0,-5000.0),hi=(+5000.0,+5000.0),
                 title='') :
        assert ieta!=iphi, "Specify either ieta or iphi"
        for item in ['coll','indices','ieta','iphi','N','lo','hi','title'] : setattr(self,item,eval(item))
        self.hname = '_'.join(coll)+'padIndexAvg'+('iEta' if ieta else 'iPhi')+indices
        self.cumname = 'cum_'+self.hname
        self.cntname = 'cnt_'+self.hname
        self.avgname = 'avg_'+self.hname
        self.moreName = self.hname
        if not self.title : self.title = 'average '+('iEta' if ieta else 'iPhi')+indices
    def uponAcceptance(self, eventVars) :
        positions = eventVars['Pos'.join(self.coll)]
        etaphiIds = eventVars['PadLocalIndices'.join(self.coll)]
        indices   = eventVars[self.indices]
        for i in indices :
            pos, etaphi = positions[i], etaphiIds[i]
            self.book.fill((pos.x(), pos.y()),
                           self.cumname, self.N, self.lo, self.hi, title=self.cumname,
                           w=(etaphi[0] if self.ieta else etaphi[1]))
            self.book.fill((pos.x(), pos.y()),
                           self.cntname, self.N, self.lo, self.hi, title=self.cntname)
    def mergeFunc(self, products) :
        num = r.gDirectory.Get(self.cumname)
        den = r.gDirectory.Get(self.cntname)
        if not num : return
        if not den : return
        eff = num.Clone('avg'+self.cumname)
        if not eff : return
        eff.SetTitle(self.title)
        eff.Divide(num,den,1,1,"B")
        # for bin in [0,self.N+1] :
        #     eff.SetBinContent(bin,0)
        #     eff.SetBinError(bin,0)
        eff.Write()
