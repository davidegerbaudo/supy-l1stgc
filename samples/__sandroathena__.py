from supy.samples import SampleHolder
sandroathena = SampleHolder()

# get the test file from Sandro:
# cp /afs/cern.ch/work/d/dimattia/public/LVL1NSW/PadIndexValidation/NSWL1Simulation.root /tmp/
sandroathena.add("Athena", '["/tmp/NSWL1Simulation.root"]', lumi=1.0e-5) # /pb

basedir = '/afs/cern.ch/user/g/gerbaudo/work/public/nsw/batch_digit/output-2013-08-05/'
sandroathena.add("Athena50k",
                 'utils.fileListFromDisk(location = "%s/*.root", isDirectory = False)'%basedir,
                 lumi=1.0e-5)
