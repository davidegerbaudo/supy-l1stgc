from supy.samples import SampleHolder
localsinglemu = SampleHolder()

localsinglemu.add("SingleMu", '["/tmp/MuonEFlat25to200GeV_17_5k_v1.root"]', lumi=1.0e-5) # /pb

# Two files from
# /afs/cern.ch/user/d/daits/workarea/public/nsw/rel_1/atlasG4.*eta_v1NSWHitsDumpAlg.root
poseneg = ['pos','neg']
localsinglemu.add('JochenSingleMu',
                  '['+','.join(['"/tmp/atlasG4.%seta_v1NSWHitsDumpAlg.root"'%pn
                                for pn in poseneg])+']',
                  lumi=1.0e-5)

localsinglemu.add('JochenSingleMuPos',
                  '['+','.join(['"/tmp/atlasG4.%seta_v1NSWHitsDumpAlg.root"'%pn
                                for pn in poseneg[:1]])+']',
                  lumi=1.0e-5)
localsinglemu.add('JochenSingleMuNeg',
                  '['+','.join(['"/tmp/atlasG4.%seta_v1NSWHitsDumpAlg.root"'%pn
                                for pn in poseneg[1:]])+']',
                  lumi=1.0e-5)
