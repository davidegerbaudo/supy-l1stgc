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
        lsteps  = []
        lsteps += [supy.steps.printer.progressPrinter(),
                   ssh.multiplicity('truthIndices', max=10),
                   ssh.multiplicity('simhitIndices', max=50),
                   ssh.multiplicity('IndicesOddSector', max=50),
                   ssh.multiplicity('IndicesEvenSector', max=50),
                   ssh.multiplicity(stsp, max=50),
                   sh.xyMap(stsp),
                   sh.xyMap(stsp, indices='IndicesOddSector'),
                   sh.xyMap(stsp, indices='IndicesEvenSector'),
                  ]
        lsteps += [ssh.multiplicity("IndicesSector%d"%s, 50) for s in config['allSectors']]
        indicesSectorLayer = ["IndicesSector%dLayer%d"%(s,l)
                              for s in config['allSectors'] for l in config['allLayers']]
        lsteps += [ssh.multiplicity(isl, 10) for isl in indicesSectorLayer]
        lsteps += [sh.xyMap(stsp, indices="IndicesOddSectorsLayer%d"%l) for l in config['allLayers']]
        lsteps += [sh.xyMap(stsp, indices="IndicesEvenSectorsLayer%d"%l) for l in config['allLayers']]

        return lsteps
    
    def listOfCalculables(self,config) :

        obj = config['objects']
        simhit = obj['stgcSimhit']
        cs = calculables.stgc
        calcs  = supy.calculables.zeroArgs(supy.calculables)
        calcs += [calculables.truth.truthIndices(label=''),
                  cs.simhitIndices(label=''),
                  ]
        calcs += [cs.Indices(simhit, "Sector%d"%s, sectors=[s,]) for s in config['allSectors']]
        calcs += [cs.Indices(simhit, "Sector%dLayer%d"%(s,l), sectors=[s,], layers=[l,])
                  for s in config['allSectors'] for l in config['allLayers']]
        calcs += [cs.Indices(simhit, "OddSectorsLayer%d"%l,
                             sectors=config['oddSectors'], layers=[l,])
                  for l in config['allLayers']]
        calcs += [cs.Indices(simhit, "EvenSectorsLayer%d"%l,
                             sectors=config['evenSectors'], layers=[l,])
                  for l in config['allLayers']]
        calcs += supy.calculables.fromCollections(cs, [simhit, ])

        return calcs
    
    def listOfSampleDictionaries(self) :
        return [samples.localsinglemu,]
    
    def listOfSamples(self,config) :
        test = True
        nEventsMax=1000 if test else -1
        return (supy.samples.specify(names='JochenSingleMu', color=r.kBlack, markerStyle = 20, nEventsMax=nEventsMax)
                )

    
    def conclude(self,pars) :
        #make a pdf file with plots from the histograms created above
        org = self.organizer(pars)
        org.scale()
        supy.plotter(org,
                     pdfFileName = self.pdfFileName(org.tag),
                     ).plotAll()
