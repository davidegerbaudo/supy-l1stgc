from supy import wrappedChain,utils,calculables,utils
import ROOT as r
import collections, math
import stgcGeometry as geo

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
class IndicesA(wrappedChain.calculable) :
    "Indices for Athena pad coord"
    @property
    def name(self) : return 'IndicesA'.join(self.fixes)
    def __init__(self, collection=('PadTdsOfflineTool_','')) :
        self.label   = 'aLabel'
        self.moreName = 'default indices'
        self.fixes   = collection
        self.stash(['nPadHits',])
    def update(self,_) :
        nPadHits = self.source[self.nPadHits]
        self.value = range(nPadHits)
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
                       + ['Pos','LocPos','SecLocPos','Pivot','Confirm','PadLocalIndices']

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
        self.stash(["padGlobal%s"%v for v in ['X','Y','Z']])
        self.pv3 = utils.root.PositionV
    def update(self, _) :
        xs = self.source[self.padGlobalX]
        ys = self.source[self.padGlobalY]
        zs = self.source[self.padGlobalZ]
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
        sectorDphi = geo.sectorDphi
        midSectorPhi = geo.midSectorPhi
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
        self.stash(['wedgeType'])
    def update(self, _) :
        confirm = 1 # see sTGCenumeration.h
        self.value = [wt==confirm for wt in self.source[self.wedgeType]]
#__________________________________________________________
class Pivot(wrappedChain.calculable) :
    @property
    def name(self) : return 'Pivot'.join(self.fixes)
    def __init__(self, collection = None) :
        self.fixes = collection
        self.stash(['wedgeType'])
    def update(self, _) :
        pivot = 0 # see sTGCenumeration.h
        self.value = [wt==pivot for wt in self.source[self.wedgeType]]
#__________________________________________________________
class PivotOrConfirm(wrappedChain.calculable) :
    @property
    def name(self) : return 'PivotOrConfirm'.join(self.fixes)
    def __init__(self, collection = None) :
        self.fixes = collection
        self.stash(['Pivot','Confirm'])
    def update(self, _) :
        ps, cs = self.source[self.Pivot], self.source[self.Confirm]
        assert not any(p==c for p,c in zip(ps,cs)),"Hits must be either Pivot or Confirm"
        self.value = ['P' if p else 'C' for p in ps]
#__________________________________________________________
class Side(wrappedChain.calculable) :
    "A side is z>0, facing LHCb; C side is z<0, facing ALICE"
    @property
    def name(self) : return 'Side'.join(self.fixes)
    def __init__(self, collection = None) :
        self.fixes = collection
        self.stash(['globalPositionZ'])
    def update(self, _) :
        zs = self.source[self.globalPositionZ]
        self.value = ['A' if z > 0.0 else 'C' for z in zs]
#__________________________________________________________
class LayersPerWedge(wrappedChain.calculable) :
    @property
    def name(self) : return 'LayersPerWedge'.join(self.fixes)
    def __init__(self, collection = None) :
        # a wedge is defined by  sector, Pivot/Confirm, and side
        self.fixes = collection
        self.stash(['layer','sectorNumber','PivotOrConfirm','Side'])
    def update(self, _) :
        layersPerWedge = collections.defaultdict(list)
        layers   = self.source[self.layer]
        sectors  = self.source[self.sectorNumber]
        pcs      = self.source[self.PivotOrConfirm]
        sides    = self.source[self.Side]
        for l,s,pc,side in zip(layers, sectors, pcs, sides) :
            layersPerWedge["S%d%s%s"%(s, pc, side)].append(l)
        self.value = dict([(k,set(v)) for k,v in layersPerWedge.iteritems()])
#__________________________________________________________
class WedgesWithNActiveLayers(wrappedChain.calculable) :
    "List of wedges that have hits in N layers"
    @property
    def name(self) : return self.label.join(self.fixes)
    def __init__(self, collection = '', nlayers = 0, label = '') :
        self.nlayers = nlayers
        self.label = "WedgesWith%dActiveLayers"%nlayers if not label else label
        self.fixes = collection
        self.stash(['LayersPerWedge'])
    def update(self, _) :
        layersPerWedge = self.source[self.LayersPerWedge]
        self.value = [w for w,l in layersPerWedge.iteritems() if self.nlayers==len(l)]
#__________________________________________________________
class WedgesWith3ActiveLayers(WedgesWithNActiveLayers) :
    def __init__(self, collection = '') :
        super(WedgesWith3ActiveLayers, self).__init__(collection, 3)
#__________________________________________________________
class WedgesWith4ActiveLayers(WedgesWithNActiveLayers) :
    def __init__(self, collection = '') :
        super(WedgesWith4ActiveLayers, self).__init__(collection, 4)
#__________________________________________________________
class Any3LayersWedgeTrigger(wrappedChain.calculable) :
    "Trigger if there is at least one wedge with at least 3 active layers"
    @property
    def name(self) : return self.label.join(self.fixes)
    def __init__(self, collection = '') :
        self.label = "Any3LayersWedgeTrigger"
        self.fixes = collection
        self.stash(['WedgesWith3ActiveLayers','WedgesWith4ActiveLayers'])
    def update(self, _) :
        self.value = any(self.source[self.WedgesWith3ActiveLayers] + self.source[self.WedgesWith4ActiveLayers])
#__________________________________________________________
class Any4LayersWedgeTrigger(wrappedChain.calculable) :
    "Trigger if there is at least one wedge with at least 4 active layers"
    @property
    def name(self) : return self.label.join(self.fixes)
    def __init__(self, collection = '') :
        self.label = "Any4LayersWedgeTrigger"
        self.fixes = collection
        self.stash(['WedgesWith4ActiveLayers'])
    def update(self, _) :
        self.value = any(self.source[self.WedgesWith4ActiveLayers])
#__________________________________________________________
class PadLocalIndices(wrappedChain.calculable) :
    "Local (ieta,iphi) indices of a pad within a singlet"
    @property
    def name(self) : return self.label.join(self.fixes)
    def __init__(self, collection = '') :
        self.label = 'PadLocalIndices'
        self.fixes = collection
        self.stash(['SecLocPos','sectorNumber','detectorNumber','wedgeId','wedgeType','layer'])
    def update(self, _) :
        pS5     = geo.midSectorPhi(5) # we are still working with the coord rotated to sector 5
        locPoss = self.source[self.SecLocPos]
        secNums = self.source[self.sectorNumber]
        detNums = self.source[self.detectorNumber]
        lss     = self.source[self.wedgeId]              # Large/Small
        pcs     = self.source[self.wedgeType]            # Pivot/Conf
        layers  = [i-1 for i in self.source[self.layer]] # [1,..,4] -> [0,...,3]
        assert all(dn in [0,1,2,3] for dn in detNums),"invalid Detector numbers %s"%str(detNums)
        assert all(ls in [0,1] and pc in [0,1] for ls,pc in zip(lss,pcs)),"invalid wedgeId/type %s, %s"%(str(lss), str(pcs))
        wedTyps = ['_'.join([geo.largeSmall2str(ls), geo.pivotConfirm2str(pc)])
                   for ls,pc in zip(lss, pcs)]
        posPars = [(p.y(), p.phi()) for p in locPoss]
        adjustZ = True
        padPars = [(geo.padPhiSize(d),               geo.padPhi0(wt, d, l),
                    geo.padLeftmostColumn(wt, d, l), geo.padRightmostColumn(wt, d, l),
                    geo.padRow0(wt, l),              geo.padHeight(wt, d),
                    geo.padZsf(wt, l) if adjustZ else 1.0
                    )
                   for pc, wt, d, l in zip(pcs, wedTyps, detNums, layers)]

        def phiOrigin(padShift, padSize) : return padShift * padSize
        def phiMpiPi2ZeroTwoPi(phi) : return phi if phi > 0. else phi + 2.0*math.pi
        def padIphi(deltaPhi, padSize) : return int(math.floor(deltaPhi/padSize))
        def adjustPadIphi(padIphi, leftmostColumn, rightmostColumn) :
            pIp, iLc, iRc = padIphi, leftmostColumn, rightmostColumn
            if   pIp<0 and pIp<iLc : return iLc
            elif pIp>0 and pIp>iRc : return iRc
            else                   : return pIp
        def localHeight(globY, lowEdgeY) : return globY - lowEdgeY
        def padIeta(localH, padHeight) : return int(localH / padHeight)
        def adjustPadIeta(padIeta, padRows) : return padRows if padIeta>padRows else padIeta
        self.value = [( padIeta(localHeight(y, pR0*zSf), pH*zSf)
                       ,padIphi(phi -pP0 - pS5 , pSi)   )
                      for (y, phi), (pSi, pP0, pLm, pRm, pR0, pH, zSf) in zip(posPars, padPars)]
#__________________________________________________________
class Pad :
    "A pad is defined by: side, sector, wedgeId(LS), wedgeType(PC), layer, ieta, iphi"
    def __init__(self, side=None, sector=None, wedgeId=None, wedgeType=None,
                 layer=None, ieta=None, iphi=None) :
        for a in ['side', 'sector', 'wedgeId', 'wedgeType', 'layer', 'ieta', 'iphi'] :
            setattr(self, a, eval(a))
        self.charge = 0.0
        self.hitIndices = []
    def __str__(self) :
        return hash(''.join([str(getattr(self,a))
                             for a in ['side', 'sector', 'wedgeId', 'wedgeType',
                                       'layer', 'ieta', 'iphi']]))
    def __hash__(self) : return hash(self.__str__())
    @property
    def id(self) : return self.__hash__()
    def addHit(self, hitIndex, hitCharge) :
        self.hitIndices.append(hitIndex)
        self.charge += hitCharge
#__________________________________________________________
class ActivePads(wrappedChain.calculable) :
    @property
    def name(self) : return self.label.join(self.fixes)
    def __init__(self, collection = '') :
        self.label = 'ActivePads'
        self.fixes = collection
        self.stash(['Side','sectorNumber','wedgeId','wedgeType','layer','PadLocalIndices','depositEnergy'])
    def update(self, _) :
        sides   = self.source[self.Side]
        sectors = self.source[self.sectorNumber]
        wIds    = self.source[self.wedgeId]
        wTs     = self.source[self.wedgeType]
        layers  = self.source[self.layer]
        iEPs    = self.source[self.PadLocalIndices]
        energies= self.source[self.depositEnergy]
        pads = dict() #collections.defaultdict(Pad)
        for i,s,se,wi,wt,l,(ieta,iphi), e in zip(range(len(sides)), sides, sectors,
                                                 wIds, wTs, layers, iEPs, energies) :
            pad = Pad(s, se, wi, wt, l, ieta, iphi)
            iD = pad.id
            if iD in pads : pads[iD].addHit(i, e)
            else :   # maybe this can be implemented with defaultdict?
                pad.addHit(i, e)
                pads[iD] = pad
            pads[pad.id].addHit(i, e)
        self.value = pads.values()
#__________________________________________________________
class ActivePadsIndices(wrappedChain.calculable) :
    @property
    def name(self) : return self.label.join(self.fixes)
    def __init__(self, collection = '') :
        self.label = 'ActivePadsIndices'
        self.fixes = collection
        self.stash(['ActivePads'])
    def update(self, _) :
        self.value = range(len(self.source[self.ActivePads]))
#__________________________________________________________
