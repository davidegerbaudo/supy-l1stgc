import supy, ROOT as r
import calculables, samples

class stgcHitLook(supy.analysis) :
    
    def listOfSteps(self,config) :
        steps  = []
        steps += [supy.steps.printer.progressPrinter(),
                  supy.steps.histos.value('Two',10,0,10),
                  ]
        return steps
    
    def listOfCalculables(self,config) :
        calcs  = supy.calculables.zeroArgs(supy.calculables)
        calcs += [supy.calculables.other.fixedValue('Two',2),
                  ]
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
