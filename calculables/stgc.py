from supy import wrappedChain,utils,calculables,utils
import ROOT as r
import math

#___________________________________________________________
class IndicesFilteredOnSector(wrappedChain.calculable) :
    def __init__(self, collection = None, filterFunctionExpression = None) :
        self.fixes = collection
        self.stash(['sectorNumber'])
        self.func = filterFunctionExpression
    def update(self,_) :
        func = eval(self.func)
        self.value = [i for i,s in enumerate(self.source[self.sectorNumber]) if func(s)]
#___________________________________________________________
class IndicesOddSector(IndicesFilteredOnSector) :
    @property
    def name(self): return 'IndicesOddSector'
    def __init__(self, collection = None) :
        super(IndicesOddSector, self).__init__(collection)
        self.func = 'lambda i : not i%2'
#___________________________________________________________
class IndicesEvenSector(IndicesFilteredOnSector) :
    @property
    def name(self): return 'IndicesEvenSector'
    def __init__(self, collection = None) :
        super(IndicesEvenSector, self).__init__(collection)
        self.func = 'lambda i : i%2'
#__________________________________________________________
class Indices(wrappedChain.calculable) :
    @property
    def name(self) : return 'Indices' + self.label
    def __init__(self, collection=('Hits_sTGC_',''), label=None, layers=[], sectors=[], pivot=None, confirm=None) :
        xyz = ['X','Y','Z']
        self.label   = label
        self.layers  = frozenset(layers)
        self.sectors = frozenset(sectors)
        self.pivot   = pivot
        self.confirm = confirm
        self.fixes   = collection
        self.stash(['n','globalTime',] \
                       +["globalPosition%s"%v for v in xyz] \
                       +["globalDirection%s"%v for v in xyz] \
                       +["localPosition%s"%v for v in xyz] \
                       +['particleEncoding','kineticEnergy','depositEnergy','StepLength'] \
                       +['unitName','detectorName','sectorNumber',
                         'wedgeId','wedgeType',
                         'unitNumber','detectorNumber',
                         'layer',
                         'padEta','padPhi',
                         'mask',
                         'stripNumber',
                         'wireNumber',] \
                       + ['Pos','LocPos','SecLocPos','Pivot','Confirm']

                   )
        self.moreName = ';'.join(filter(lambda x:x,
                                        ["Layer in %s"%str(list(self.layers)) if self.layers else '',
                                         "Sector in %s"%str(list(self.sectors)) if self.sectors else '',
                                         'Pivot' if self.pivot else '',
                                         'Confirm' if self.confirm else '',
                                         ])
                                 )
    def update(self,_) :
        layer   = self.source[self.layer]
        sector  = self.source[self.sectorNumber]
        pivot   = self.source[self.Pivot]
        confirm = self.source[self.Confirm]
        self.value = filter( lambda i: \
                                 ( (not self.layers) or (layer.at(i) in self.layers)    ) and \
                                 ( (not self.sectors) or (sector.at(i) in self.sectors) ) and \
                                 ( (not self.pivot) or pivot[i]                         ) and \
                                 ( (not self.confirm) or confirm[i]                     )
                             ,
                             range(layer.size()) )
class simhitIndices(Indices):
    @property
    def name(self): return 'simhitIndices' + self.label
#__________________________________________________________
class Pos(wrappedChain.calculable) :
    @property
    def name(self) : return 'Pos'.join(self.fixes)
    def __init__(self, collection) :
        self.fixes = collection
        self.stash(["globalPosition%s"%v for v in ['X','Y','Z']])
        self.pv3 = utils.root.PositionV
    def update(self, _) :
        xs = self.source[self.globalPositionX]
        ys = self.source[self.globalPositionY]
        zs = self.source[self.globalPositionZ]
        self.value = [self.pv3(x,y,z) for x,y,z in zip(xs,ys,zs)]
#__________________________________________________________
class LocPos(wrappedChain.calculable) :
    @property
    def name(self) : return 'LocPos'.join(self.fixes)
    def __init__(self, collection) :
        self.fixes = collection
        self.stash(["localPosition%s"%v for v in ['X','Y','Z']])
        self.pv3 = utils.root.PositionV
    def update(self, _) :
        xs = self.source[self.localPositionX]
        ys = self.source[self.localPositionY]
        zs = self.source[self.localPositionZ]
        self.value = [self.pv3(x,y,z) for x,y,z in zip(xs,ys,zs)]
#__________________________________________________________
class SecLocPos(wrappedChain.calculable) :
    "Position in the local coordinates within the Sector (wrt. the sector point of symmetry)"
    @property
    def name(self) : return 'SecLocPos'.join(self.fixes)
    def __init__(self, collection) :
        self.fixes = collection
        self.stash(['sectorNumber'] + ["globalPosition%s"%v for v in ['X','Y','Z']])
        self.pv3 = utils.root.PositionV
    def update(self, _) :
        xs  = self.source[self.globalPositionX]
        ys  = self.source[self.globalPositionY]
        zs  = self.source[self.globalPositionZ]
        sns = self.source[self.sectorNumber]
        sectorDphi = 2.0*math.pi/16.
        def midSectorPhi(sec) : return (sec-1)*sectorDphi # sector N starts from 1
        targetPhi = midSectorPhi(5) # sector 5 is the one centered on the y axis
        def rotationAngle(sec) : return midSectorPhi(sec) - targetPhi
        repv = r.Math.RhoEtaPhiVector
        vsXyz = [self.pv3(x,y,z) for x,y,z in zip(xs,ys,zs)] # intermediate vector to simplify rotation
        vsRep = [repv(v.rho(), v.eta(), v.phi()).SetPhi(v.phi() - rotationAngle(s)) for v,s in zip(vsXyz, sns)]
        self.value = [self.pv3(v.x(),v.y(),v.z()) for v in vsRep]
#__________________________________________________________
class GenericPivotConfirm(wrappedChain.calculable) :
    "Used to emulate the pivot confirm bit; will be dropped once we have this piece of info from the geometry"
    def __init__(self, collection=None, minZ=None, maxZ=None) :
        self.fixes = collection
        self.stash(['globalPositionZ'])
        self.minZ = minZ
        self.maxZ = maxZ
    def update(self, _) :
        self.value = [((abs(z) >= self.minZ if self.minZ!=None else True)
                       and
                       (abs(z) <  self.maxZ if self.maxZ!=None else True))
                      for z in self.source[self.globalPositionZ]]
#__________________________________________________________
class SmallConfirm(GenericPivotConfirm) :
    @property
    def name(self) : return 'SmallConfirm'.join(self.fixes)
    def __init__(self, collection = None) :
        super(SmallConfirm, self).__init__(collection)
        self.minZ = 7000.
        self.maxZ = 7100.
#__________________________________________________________
class SmallPivot(GenericPivotConfirm) :
    @property
    def name(self) : return 'SmallPivot'.join(self.fixes)
    def __init__(self, collection = None) :
        super(SmallPivot, self).__init__(collection)
        self.minZ = 7300.
        self.maxZ = 7400.
#__________________________________________________________
class LargePivot(GenericPivotConfirm) :
    @property
    def name(self) : return 'LargePivot'.join(self.fixes)
    def __init__(self, collection = None) :
        super(LargePivot, self).__init__(collection)
        self.minZ = 7400.
        self.maxZ = 7500.
#__________________________________________________________
class LargeConfirm(GenericPivotConfirm) :
    @property
    def name(self) : return 'LargeConfirm'.join(self.fixes)
    def __init__(self, collection = None) :
        super(LargeConfirm, self).__init__(collection)
        self.minZ = 7600.
        self.maxZ = 7800.
#__________________________________________________________
class Confirm(wrappedChain.calculable) :
    @property
    def name(self) : return 'Confirm'.join(self.fixes)
    def __init__(self, collection = None) :
        self.fixes = collection
        self.stash(['SmallConfirm','LargeConfirm'])
    def update(self, _) :
        self.value = [sc or lc for sc,lc in zip(self.source[self.SmallConfirm], self.source[self.LargeConfirm])]
#__________________________________________________________
class Pivot(wrappedChain.calculable) :
    @property
    def name(self) : return 'Pivot'.join(self.fixes)
    def __init__(self, collection = None) :
        self.fixes = collection
        self.stash(['SmallPivot','LargePivot'])
    def update(self, _) :
        self.value = [sp or lp for sp,lp in zip(self.source[self.SmallPivot], self.source[self.LargePivot])]
#__________________________________________________________



#
# todo : define calculables for micromega hits
#
# -- collection = ('Hits_MM_','')
# -- stashVars = [
# -- 'n',
# -- 'globalTime',
# -- 'globalPositionX',
# -- 'globalPositionY',
# -- 'globalPositionZ',
# -- 'globalDirectionX',
# -- 'globalDirectionY',
# -- 'globalDirectionZ',
# --
# -- 'localPositionX',
# -- 'localPositionY',
# -- 'localPositionZ',
# --
# -- 'particleEncoding',
# -- 'kineticEnergy',
# -- 'depositEnergy',
# -- 'StepLength',
# -- ]
