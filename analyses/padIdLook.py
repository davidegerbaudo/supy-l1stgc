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
        fields =                    [ 'PadOffTool']
        objects =  dict(zip(fields, [('PadTdsOfflineTool_',''),]))
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
        pot      =  obj['PadOffTool']
        poti = 'IndicesA'.join(pot)
        potp = 'Pos'.join(pot)
        lsteps  = []
        lsteps += [supy.steps.printer.progressPrinter()]
        lsteps += [ssh.multiplicity(b) for b in branchnames]
        lsteps += [sh.absZ(potp, 100, 7000, 8000, poti)]
        lsteps += [sh.absZ(potp, 100, 7100, 7310, poti)]
        lsteps += [sh.absZ(potp, 100, 7460, 7680, poti)]
        lsteps += [ssh.value('Small'.join(pot), 3, -0.5, 2.5, poti)]
        lsteps += [ssh.value('Sector'.join(pot), 21, -0.5, 20.5, poti)]
        lsteps += [sh.yVsX((potp, potp), poti),]
        lsteps += [ssh.multiplicity("IndicesOddL%d"%l)  for l in range(1,4+1)]
        lsteps += [ssh.multiplicity("IndicesEvenL%d"%l) for l in range(1,4+1)]
        lsteps += [sh.yVsX((potp, potp), "IndicesOddL%d"%l)  for l in range(1,4+1)]
        lsteps += [sh.yVsX((potp, potp), "IndicesEvenL%d"%l) for l in range(1,4+1)]
        lsteps += [sh.padIndexAvg(pot, "IndicesOddL%d"%l, ieta=True)  for l in range(1,4+1)]
        lsteps += [sh.padIndexAvg(pot, "IndicesOddL%d"%l, iphi=True)  for l in range(1,4+1)]
        lsteps += [sh.padIndexAvg(pot, "IndicesEvenL%d"%l, ieta=True) for l in range(1,4+1)]
        lsteps += [sh.padIndexAvg(pot, "IndicesEvenL%d"%l, iphi=True) for l in range(1,4+1)]
        return lsteps
    def listOfCalculables(self,config) :
        obj       = config['objects']
        pot      =  obj['PadOffTool']
        cs = calculables.stgc
        calcs  = supy.calculables.zeroArgs(supy.calculables)
        calcs += supy.calculables.fromCollections(cs, [pot, ])
        calcs += [cs.IndicesOddSectorLayer( pot, "L%d"%l, [l]) for l in range(1,4+1)]
        calcs += [cs.IndicesEvenSectorLayer(pot, "L%d"%l, [l]) for l in range(1,4+1)]
        return calcs
    def listOfSampleDictionaries(self) :
        return [samples.localsinglemu, samples.sandroathena]
    def listOfSamples(self,config) :
        test = False #True
        nEventsMax=1000 if test else None
        return (supy.samples.specify(names='Athena50k', color=r.kBlack, markerStyle = 2,
                                     nEventsMax=nEventsMax)
                )
    def conclude(self,pars) :
        org = self.organizer(pars)
        org.scale()
        supy.plotter(org,
                     pdfFileName = self.pdfFileName(org.tag),
                     doLog=False,
                     blackList = ['lumiHisto','xsHisto','nJobsHisto',
                                  'cnt_.*', 'cum_.*'],
                     ).plotAll()
