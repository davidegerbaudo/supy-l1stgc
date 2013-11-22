
# Calculables for the ntuples produced by the pad time delay
# simulation (TDS) tool: TrigT1/TrigT1NSWSimTools/PadTdsOfflineTool
#
# davide.gerbaudo@gmail.com
# Nov 2013

from supy import wrappedChain,utils,calculables,utils
import ROOT as r
import collections, math
import stgcGeometry as geo

#__________________________________________________________
class Pos(wrappedChain.calculable) :
    @property
    def name(self) : return 'Pos'.join(self.fixes)
    def __init__(self, collection) :
        self.fixes = collection
        self.stash(["padTruthHitGlobal%s"%v for v in ['X','Y','Z']])
        self.pv3 = utils.root.PositionV
    def update(self, _) :
        xs = self.source[self.padTruthHitGlobalX]
        ys = self.source[self.padTruthHitGlobalY]
        zs = self.source[self.padTruthHitGlobalZ]
        self.value = [self.pv3(x,y,z) for x,y,z in zip(xs,ys,zs)]
#__________________________________________________________
class Sector(wrappedChain.calculable) :
    @property
    def name(self) : return 'Sector'.join(self.fixes)
    def __init__(self, collection) :
        self.fixes = collection
        self.stash(['Pos'])
    def update(self, _) :
        positions = self.source[self.Pos]
        pi, twopi = math.pi, 2.0*math.pi
        fabs, atan2, deg2rad = math.fabs, math.atan2, math.radians
        def phi_zero_2pi(phi) :
            while phi <  0.0   : phi += twopi
            while phi >= twopi : phi -= twopi
            return phi
        def pos2sec(pos) :
            "determine the sector number from the global position"
            sixteenth = twopi/16.0
            phi = phi_zero_2pi(atan2(pos.Y(), pos.X()))
            secPhiCenters = dict([(s, sixteenth*float(s-1)) for s in range(1, 1+16)])
            secPhiDists   = dict([(s, phi_zero_2pi(phi-c)) for s,c in secPhiCenters.iteritems()])
            closestSec = sorted(secPhiDists, key=secPhiDists.get)[0] # access keys sorted by value
            sec, dist = closestSec, secPhiDists[closestSec]
            isSmall, isOdd = fabs(pos.Z()) < 7400., sec%2==0
            isLarge, isEven = not isSmall, not isOdd
            secDphiWidth = deg2rad(22.5 if isSmall else 33.0)
            if isSmall and isOdd : print "warning: odd %d should be large (z=%f)"%(sec, pos.Z())
            if isLarge and isEven : print "warning: even %d should be small (z=%f)"%(sec, pos.Z())
            if dist > 0.5*secDphiWidth : print "warning: %s>half-width %f"%(dist, 0.5*secDphiWidth)
            return closestSec
        self.value = [pos2sec(p) for p in positions]
#__________________________________________________________
class sectorNumber(wrappedChain.calculable) :
    "compatibility with the hitdumper leafname"
    @property
    def name(self) : return 'sectorNumber'.join(self.fixes)
    def __init__(self, collection) :
        self.fixes = collection
        self.stash(['Sector'])
    def update(self, _) :
        self.value = self.source[self.Sector]
