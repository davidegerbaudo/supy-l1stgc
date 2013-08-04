from supy.samples import SampleHolder
sandroathena = SampleHolder()

# get the test file from Sandro:
# cp /afs/cern.ch/work/d/dimattia/public/LVL1NSW/PadIndexValidation/NSWL1Simulation.root /tmp/
sandroathena.add("Athena", '["/tmp/NSWL1Simulation.root"]', lumi=1.0e-5) # /pb
