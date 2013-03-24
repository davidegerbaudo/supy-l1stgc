import supy, ROOT as r
import calculables, steps, samples

class stgcHitLook(supy.analysis) :

    def parameters(self) :
        fields =                    [ 'stgcSimhit',     ]
        objects =  dict(zip(fields, [('Hits_sTGC_',''), ]))
        return {
            'objects'  : objects,
            'allSectors' : range(1,16+1),
            }
    def listOfSteps(self,config) :
        sh  = steps.histos
        ssh = supy.steps.histos
        lsteps  = []
        lsteps += [supy.steps.printer.progressPrinter(),
                   ssh.multiplicity('truthIndices', max=10),
                   ssh.multiplicity('simhitIndices', max=50),
                   ssh.multiplicity('IndicesOddSector', max=50),
                   ssh.multiplicity('IndicesEvenSector', max=50),
                   ssh.multiplicity('Hits_sTGC_Pos', max=50),
                   sh.xyMap('Hits_sTGC_Pos'),
                   sh.xyMap('Hits_sTGC_Pos', indices='IndicesOddSector'),
                   sh.xyMap('Hits_sTGC_Pos', indices='IndicesEvenSector'),
                  ]
        lsteps += [ssh.multiplicity("IndicesSector%d"%s, 50) for s in config['allSectors']]
        lsteps += [ssh.value(var='Hits_sTGC_layer', indices='simhitIndices', N=21, low=-0.5, up=20.5)]
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
        calcs += supy.calculables.fromCollections(cs, [simhit, ])

        return calcs
    
    def listOfSampleDictionaries(self) :
        return [samples.localsinglemu,]
    
    def listOfSamples(self,config) :
        return (supy.samples.specify(names="SingleMu", color=r.kBlack, markerStyle = 20)
                )

    
    def conclude(self,pars) :
        #make a pdf file with plots from the histograms created above
        org = self.organizer(pars)
        org.scale()
        supy.plotter(org,
                     pdfFileName = self.pdfFileName(org.tag),
                     ).plotAll()
