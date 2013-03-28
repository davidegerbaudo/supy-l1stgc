from supy.samples import SampleHolder
localsinglemu = SampleHolder()

localsinglemu.add("SingleMu", '["/tmp/MuonEFlat25to200GeV_17_5k_v1.root"]', lumi=1.0e-5) # /pb

# Two files from
# /eos/atlas/user/g/gerbaudo/trigger/nsw/2013-03-27/atlasG4.pos.NSWHitsDumper.root
# (produced from ~jomeyer/public/NSW/atlasG4.*.hits.pool.root)
poseneg = ['pos','neg']
localsinglemu.add('JochenSingleMu',
                  '['+','.join(['"/tmp/atlasG4.%s.NSWHitsDumper.root"'%pn for pn in poseneg])+']',
                  lumi=1.0e-5)

localsinglemu.add('JochenSingleMuPos',
                  '['+','.join(['"/tmp/atlasG4.%s.NSWHitsDumper.root"'%pn for pn in poseneg[:1]])+']',
                  lumi=1.0e-5)
localsinglemu.add('JochenSingleMuNeg',
                  '['+','.join(['"/tmp/atlasG4.%s.NSWHitsDumper.root"'%pn for pn in poseneg[1:]])+']',
                  lumi=1.0e-5)
