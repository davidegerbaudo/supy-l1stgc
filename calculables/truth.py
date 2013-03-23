from supy import wrappedChain,utils,calculables
import ROOT as r


#___________________________________________________________
class VertexPosition(wrappedChain.calculable) :
    # this class might not be needed if I use supy.calculables.fromCollections
    @property
    #def name(self) : return "vertex"
    def __init__(self, collection=('TruthVertex_','')):
        self.pv3 = r.Math.PositionVector3D
        self.fixes = collection
        self.stash(['n','X','Y','Z','T','Id'])
    def update(self, _) :
        xs, ys, zs = self.source[self.X], self.source[self.Y], self.source[self.Z]
        self.value = [self.pv3(x,y,z) for x,y,z in zip(xs, ys, zs)]
#___________________________________________________________
class Indices(wrappedChain.calculable) :
    @property
    def name(self) : return "GenIndices_" + self.label
    def __init__(self, collection=('TruthParticle_',''),
                 label = None, pdgs = [], status = []) :
        self.label = label
        self.PDGs = frozenset(pdgs)
        self.status = frozenset(status)
        self.fixes = collection
        self.stash(['Pt','Eta','Phi','E','M','Pdg','Status','Production_vertex_id','End_vertex_id'])
        self.moreName = "; ".join(["pdgId in %s" %str(list(self.PDGs)),
                                   "status in %s"%str(list(self.status)),
                                   ])
    def update(self,_) :
        pdg = self.source[self.Pdg]
        status = self.source[self.Status]
        self.value = filter( lambda i: \
                                 ( (not self.PDGs) or (pdg.at(i) in self.PDGs) ) and \
                                 ( (not self.status) or (status.at(i) in self.status) )
                             ,
                             range(pdg.size()) )

class truthIndices(Indices) :
    @property
    def name(self) : return "truthIndices" + self.label
