from supy.samples import SampleHolder
localsinglemu = SampleHolder()

localsinglemu.add("SingleMu", '["/tmp/MuonEFlat25to200GeV_17_5k_v1.root"]', lumi=1.0e-5) # /pb


localsinglemu.add('JochenSingleMu',
                  '['+','.join(['"/tmp/atlasG4.%seta_v1NSWHitsDumpAlg.root"'%pn
                                for pn in ['pos','neg']])+']',
                  lumi=1.0e-5)
