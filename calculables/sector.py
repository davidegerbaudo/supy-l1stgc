# Sector-related calculables, that should work for both HitDumper
# ntuples and TDS ntuples.
#
# davide.gerbaudo@gmail.com
# Nov 2013

from supy import wrappedChain

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

