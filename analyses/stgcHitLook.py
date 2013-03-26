import supy, ROOT as r
import calculables, steps, samples

class stgcHitLook(supy.analysis) :

    def parameters(self) :
        fields =                    [ 'stgcSimhit',     ]
        objects =  dict(zip(fields, [('Hits_sTGC_',''), ]))
        return {
            'objects'  : objects,
            'allSectors' : range(1, 16+1),
            'oddSectors'  : [s for s in range(1, 16+1) if     s%2],
            'evenSectors' : [s for s in range(1, 16+1) if not s%2],
            'allLayers' :  range(1, 4+1),
            }
    def listOfSteps(self,config) :
        sh, ssh = steps.histos, supy.steps.histos
        obj = config['objects']
        stsh = obj['stgcSimhit']
        stsi = 'simhitIndices'
        stsp = 'Pos'.join(stsh)
        stslp = 'LocPos'.join(stsh)
        lsteps  = []
        lsteps += [supy.steps.printer.progressPrinter(),
                   ssh.multiplicity('IndicesOddSector', max=50),
                   ssh.multiplicity('IndicesEvenSector', max=50),
                   sh.xyMap(stsp, indices='IndicesOddSector'),
                   sh.xyMap(stsp, indices='IndicesEvenSector'),
                  ]
#        lsteps += [ssh.multiplicity("IndicesSector%d"%s, 50) for s in config['allSectors']]
        allLayers = config['allLayers']
        indicesSectorLayer = ["IndicesSector%dLayer%d"%(s,l)
                              for s in config['allSectors'] for l in allLayers]
        indicesEoCpSectorsLayer = ["Indices%s%sSectorsLayer%d"%(eo,cp,l)
                                   for eo in ['Even','Odd']
                                   for cp in ['Confirm','Pivot']
                                   for l in allLayers]
        lsteps += [sh.xyMap(stsp, indices=idx) for idx in indicesEoCpSectorsLayer]
        lsteps += [sh.eta(stsp, 100, 1.0, 3.0, idx) for idx in indicesEoCpSectorsLayer]
        # lsteps += [sh.xyMap(stslp, indices=idx, xLo=-2.0,xHi=+2.0, yLo=-1500.0,yHi=+1500.0)
        #            for idx in indicesEoCpSectorsLayer]

        return lsteps

    def listOfCalculables(self,config) :

        obj = config['objects']
        simhit = obj['stgcSimhit']
        cs = calculables.stgc
        calcs  = supy.calculables.zeroArgs(supy.calculables)
        calcs += [calculables.truth.truthIndices(label=''),
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

        return calcs

    def listOfSampleDictionaries(self) :
        return [samples.localsinglemu,]

    def listOfSamples(self,config) :
        test = False #True
        nEventsMax=10000 if test else None
        return (supy.samples.specify(names='JochenSingleMuPos', color=r.kBlack, markerStyle = 2, nEventsMax=nEventsMax)
                )


    def conclude(self,pars) :
        #make a pdf file with plots from the histograms created above
        org = self.organizer(pars)
        org.scale()
        supy.plotter(org,
                     pdfFileName = self.pdfFileName(org.tag),
                     ).plotAll()
