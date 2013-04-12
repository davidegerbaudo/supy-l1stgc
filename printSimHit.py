#!/bin/env python

import ROOT as r
r.gROOT.SetBatch(1)
inputFileNames = ['/tmp/SingleMuPC0402_1000evt_digit_6Bits.root'
                  ,'/tmp/atlasG4.pos.NSWHitsDumper.root'
                  ]
inputTreeName='NSWHitsTree'

collection=('Hits_sTGC_','')
branchNames = [b.join(collection) for b in ['layer','globalPositionZ']]
branchNames.append('t_Type_sTGC')

for inputFileName in inputFileNames :
    inputFile = r.TFile.Open(inputFileName)
    inputTree = inputFile.Get(inputTreeName)
    print "input file : %s" % inputFileName
    for iEntry in range(10) :
        inputTree.GetEntry(iEntry)
        branches = [[x for x in getattr(inputTree, b)] if hasattr(inputTree,b) else []
                    for b in branchNames]
        print "entry %d : "%iEntry +', '.join(["%s[%d]"%(bn,len(br)) for bn,br in zip(branchNames, branches)])
