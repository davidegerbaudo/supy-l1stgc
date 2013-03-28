#import copy,array,os,collections
#import ROOT as r
from supy import steps
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
