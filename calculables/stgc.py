from supy import wrappedChain,utils,calculables
import ROOT as r

#___________________________________________________________
class Indices(wrappedChain.calculable) :
    @property
    def name(self) : return 'Indices' + self.label
    def __init__(self, collection=('Hits_sTGC_',''), label=None, layers=[], sectors=[]) :
        xyz = ['X','Y','Z']
        self.label = label
        self.layers = frozenset(layers)
        self.sectors = frozenset(sectors)
        self.fixes = collection
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
                         'wireNumber',
                         ])
        self.moreName = ';'.join(filter(lambda x:x,
                                        ["Layer in %s"%str(list(self.layers)) if self.layers else '',
                                         "Sector in %s"%str(list(self.sectors)) if self.sectors else '',
                                         ])
                                 )

    def update(self,_) :
        layer = self.source[self.layer]
        sector = self.source[self.sectorNumber]
        self.value = filter( lambda i: \
                                 ( (not self.layers) or (layer.at(i) in self.layers) ) and \
                                 ( (not self.sectors) or (sector.at(i) in self.sectors) )
                             ,
                             range(layer.size()) )
class simhitIndices(Indices):
    @property
    def name(self): return 'simhitIndices' + self.label

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
