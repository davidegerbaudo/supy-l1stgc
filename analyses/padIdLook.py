import supy, ROOT as r
import calculables, steps, samples
import math


# runNumber
# eventNumber
branchnames = ["PadTdsOfflineTool_%s"%l
               for l in [#'nPadHits',
                         'padGlobalX',
                         'padGlobalY',
                         'padGlobalZ',
                         'padEtaIdFromOfflineId',
                         'padPhiIdFromOfflineId',
                         'offlineIdPadEtaIdConverted',
                         'offlineIdPadPhiIdConverted',
                         'padEtaIdFromOldSimu',
                         'padPhiIdFromOldSimu',
                         ]]


class padIdLook(supy.analysis) :

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
        truthP4 = 'P4'.join(truthPart)
        truthIdx = 'truthIndices'
        pi = math.pi

        lsteps  = []
        lsteps += [supy.steps.printer.progressPrinter()]
        lsteps += [ssh.multiplicity(b) for b in branchnames]

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

        return calcs

    def listOfSampleDictionaries(self) :
        return [samples.localsinglemu, samples.sandroathena]

    def listOfSamples(self,config) :
        test = False #True
        nEventsMax=1000 if test else None
        return ( supy.samples.specify(names='Athena', color=r.kBlack, markerStyle = 2, nEventsMax=nEventsMax)
                )


    def conclude(self,pars) :
        #make a pdf file with plots from the histograms created above
        org = self.organizer(pars)
        org.scale()
        supy.plotter(org,
                     pdfFileName = self.pdfFileName(org.tag),
                     doLog=False,
                     blackList = ['lumiHisto','xsHisto','nJobsHisto','cnt_.*', 'cum_.*'],
                     ).plotAll()
