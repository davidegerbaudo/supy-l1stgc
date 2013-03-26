import supy, ROOT as r
import calculables, steps, samples

class stgcHitLook(supy.analysis) :

    def parameters(self) :
        fields =                    [ 'stgcSimhit',     'truthPart']
        objects =  dict(zip(fields, [('Hits_sTGC_',''), ('TruthParticle_','')]))
        return {
            'objects'  : objects,
            'allSectors' : range(1, 16+1),
            'oddSectors'  : [s for s in range(1, 16+1) if     s%2],
            'evenSectors' : [s for s in range(1, 16+1) if not s%2],
            'allLayers' :  range(1, 4+1),
            }
    def listOfSteps(self,config) :
        sh, ssh, ssf = steps.histos, supy.steps.histos, supy.steps.filters
        obj       = config['objects']
        stsh      = obj['stgcSimhit']
        truthPart = obj['truthPart']
        stsi = 'simhitIndices'
        stsp = 'Pos'.join(stsh)
        stslp = 'LocPos'.join(stsh)
        stsslp = 'SecLocPos'.join(stsh)

        lsteps  = []
        lsteps += [supy.steps.printer.progressPrinter(),
                   # supy.steps.histos.multiplicity('truthIndices', max=10),
                   # ssh.multiplicity('IndicesOddSector', max=50),
                   # ssh.multiplicity('IndicesEvenSector', max=50),
                   # sh.xyMap(stsp, indices='IndicesOddSector'),
                   # sh.xyMap(stsp, indices='IndicesEvenSector'),
                  ]
        allLayers = config['allLayers']
        indicesSectorLayer = ["IndicesSector%dLayer%d"%(s,l)
                              for s in config['allSectors'] for l in allLayers]
        indicesEoCpSectorsLayer = ["Indices%s%sSectorsLayer%d"%(eo,cp,l)
                                   for eo in ['Even','Odd']
                                   for cp in ['Confirm','Pivot']
                                   for l in allLayers]
        # lsteps += [sh.xyMap(stsp, indices=idx) for idx in indicesEoCpSectorsLayer]
        # lsteps += [sh.eta(stsp, 100, 1.0, 3.0, idx) for idx in indicesEoCpSectorsLayer]
        # lsteps += [sh.xyMap(stsslp, indices=idx) for idx in indicesEoCpSectorsLayer]
        lsteps += [ssf.multiplicity('truthIndices', min=1)] # need at least one truth muon
        lsteps += [ssh.eta('P4'.join(truthPart), 100, 1.0, 3.0, 'truthIndices', 0),
                   ssh.pt('P4'.join(truthPart),  100, 0.0*1e3, 100.0*1.e3, 'truthIndices', 0),
                   sh.etaPhiMap('P4'.join(truthPart), indices='truthIndices', index=0)]
        lsteps += [ssf.value('BasicWedgeTrigger3L'.join(stsh), min=1)]
        lsteps += [ssh.eta('P4'.join(truthPart), 100, 1.0, 3.0, 'truthIndices', 0),
                   ssh.pt('P4'.join(truthPart),  100, 0.0*1e3, 100.0*1.e3, 'truthIndices', 0),
                   sh.etaPhiMap('P4'.join(truthPart), indices='truthIndices', index=0)]
        lsteps += [ssf.value('BasicWedgeTrigger4L'.join(stsh), min=1)]
        lsteps += [ssh.eta('P4'.join(truthPart), 100, 1.0, 3.0, 'truthIndices', 0),
                   ssh.pt('P4'.join(truthPart),  100, 0.0*1e3, 100.0*1.e3, 'truthIndices', 0),
                   sh.etaPhiMap('P4'.join(truthPart), indices='truthIndices', index=0)]

        return lsteps

    def listOfCalculables(self,config) :

        obj       = config['objects']
        simhit    = obj['stgcSimhit']
        truthPart = obj['truthPart']
        cs = calculables.stgc
        calcs  = supy.calculables.zeroArgs(supy.calculables)
        calcs += [calculables.truth.truthIndices(pdgs=[+13, -13]),
                  cs.simhitIndices(label=''),
                  ]
        allSectors, allLayers = config['allSectors'], config['allLayers']
        oddSectors, evenSectors = config['oddSectors'], config['evenSectors']
        calcs += [cs.Indices(simhit, "Sector%d"%s, sectors=[s,]) for s in allSectors]
        calcs += [cs.Indices(simhit, "Sector%dLayer%d"%(s,l), sectors=[s,], layers=[l,])
                  for s in allSectors for l in allLayers]
        calcs += [cs.Indices(simhit, "OddSectorsLayer%d"%l,
                             sectors=config['oddSectors'], layers=[l,])
                  for l in config['allLayers']]
        calcs += [cs.Indices(simhit, "EvenSectorsLayer%d"%l,
                             sectors=config['evenSectors'], layers=[l,])
                  for l in config['allLayers']]

        calcs += [cs.Indices(simhit, eok+pck+"SectorsLayer%d"%l,
                             sectors=eos, layers=[l,],pivot=pcv, confirm=not pcv)
                  for eok, eos in zip(['Even',  'Odd'    ], [evenSectors, oddSectors])
                  for pck, pcv in zip(['Pivot', 'Confirm'], [True,        False     ])
                  for l in allLayers]
        calcs += supy.calculables.fromCollections(cs, [simhit, ])
        calcs += supy.calculables.fromCollections(calculables.truth, [truthPart])
        calcs += [cs.BasicWedgeTrigger(simhit, nl) for nl in [3,4]]

        return calcs

    def listOfSampleDictionaries(self) :
        return [samples.localsinglemu,]

    def listOfSamples(self,config) :
        test = True #False
        nEventsMax=1000 if test else None
        return (supy.samples.specify(names='JochenSingleMuPos', color=r.kBlack, markerStyle = 2, nEventsMax=nEventsMax)
                )


    def conclude(self,pars) :
        #make a pdf file with plots from the histograms created above
        org = self.organizer(pars)
        org.scale()
        supy.plotter(org,
                     pdfFileName = self.pdfFileName(org.tag),
                     ).plotAll()
