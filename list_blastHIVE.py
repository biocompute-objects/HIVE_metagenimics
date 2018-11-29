#!/usr/bin/env python3.5
# -*- coding: utf-8 -*-

################################################################################
                            ##list_censusHIVE##
""""Submit a CensuScopr Job and waits for completion before submitting the next one in a list"""
################################################################################

from cookielib import CookieJar
import urllib, urllib2, re, csv, requests, time, os, json


login      = 'hadley_king@gwmail.gwu.edu'
os.system("stty -echo")
pwd        = 'T3mpl3Gr@d17'#raw_input('Enter Password:')
os.system("stty echo")
lstfile = '/Users/hadleyking/Downloads/filteredContigs.csv'
gutDB   = '553399'
hive_URL   = 'https://hive.biochemistry.gwu.edu/dna.cgi?'
opener     = urllib2.build_opener(urllib2.HTTPCookieProcessor(CookieJar()))

#______________________________________________________________________________#
def logInHIVE ( login, pwd ):
    """Login to HIVE """
    log_in     = str('api=0&cmdr=login&login='+login+'&pswd='+pwd)
    response   = opener.open(hive_URL, log_in)
    print "login successfull"
    return response
#______________________________________________________________________________#
def readIDlist ( file ):
    """reads list of Obj Ids"""
    samples = {}
    with open(file, 'rU') as lst:
        read = csv.reader(lst)
        for i in read: 
            sample = i[1].split('_')[0]
            objid = i[0]
            if sample in samples.keys(): samples[sample].append(objid)
            else: samples[sample] = [objid]
    return samples
#______________________________________________________________________________#
def submitProcess ( sample, query1, nt_db ):
    """Submits the API request for a process computation"""
    print "Creating process Alignment Object\n" 
    processName = sample
    process_valuz = [
        ('cmdr','-qpProcSubmit'),
        ('raw','1'),
        ('prop.svc-align-blast.query.1.1',nt_db),
        ('prop.svc-align-blast.subject.1.1',query1),
        ('prop.svc-align-blast.name.1',sample+'_unalignedBLAST'),
        ('prop.svc-align-blast._type','svc-align-blast'),
        ('prop.svc-align-blast.alignSelector.36','svc-align-blast'),
        ('prop.svc-align-blast.force_reindex.37','0'),
        ('prop.svc-align-blast.submitter.40','dna-hexagon&cmdMode=blast-bacteria'),
        ('prop.svc-align-blast.maxNumberQuery.15','all'),
        ('prop.svc-align-blast.batch_svc.6','single'),
        ('prop.svc-align-blast.blastProgram.7','blastn'),
        ('prop.svc-align-blast.evalueFilter.12','1e-10'),
        ('prop.svc-align-blast.cmdLine.9','-task megablast -num_threads 1'),
        ('prop.svc-align-blast.scissors.26','hiveseq'),
        ('prop.svc-align-blast.complexityRefEntropy.10.1.0','1.2'),
        ('prop.svc-align-blast.complexityRefWindow.10.1.0','30'),
        ('prop.svc-align-blast.acceptNNNQuaTrheshold.10.1.0','1'),
        ('prop.svc-align-blast.complexityEntropy.10.0.0','1.2'),
        ('prop.svc-align-blast.complexityWindow.10.0.0','30'),
        ('prop.svc-align-blast.maximumPercentLowQualityAllowed.10.0.0','0'),
        ('prop.svc-align-blast.keepAllMatches.13','4'),
        ('prop.svc-align-blast.maxHitsPerRead.14','200'),
        ('prop.svc-align-blast.minMatchLen.16.0','75'),
        ('prop.svc-align-blast.minMatchUnit.16.0','0'),
        ('prop.svc-align-blast.maxMissQueryPercent.17.0','15'),
        ('prop.svc-align-blast.considerGoodSubalignments.17.0','1'),
        ('prop.svc-align-blast.num_alignments.19','10'),
        ('prop.svc-align-blast.random_seed.23','0'),
        ('prop.svc-align-blast.resolveConflicts.24.1','2'),
        ('prop.svc-align-blast.resolveConflictsScore.24.2','2'),
        ('prop.svc-align-blast.resolveConfictsUnique.24.0','1'),
        ('prop.svc-align-blast.scoreFilter.27','None'),
        ('prop.svc-align-blast.splitType.31.3','sequences'),
        ('prop.svc-align-blast.nrepeat.31.0','1'),
        ('prop.svc-align-blast.splitField.31.1','query'),
        ('prop.svc-align-blast.splitSize.31.2','4000'),
        ('prop.svc-align-blast.isPostponed.34.3','0'),
        ('prop.svc-align-blast.reqPriority.34.7','0'),
        ('prop.svc-align-blast.split.30','query'),
        ('prop.svc-align-blast.seedSize.28','28'),
        ('prop.svc-align-blast.slice.29','4000'),
        ('prop.svc-align-blast.svc','dna-alignx')
    ]

    process_comand = urllib.urlencode(process_valuz)
    print process_comand
    response7 = opener.open(hive_URL, process_comand)
    pro_id = response7.read()
    pro_id = pro_id.split(',')[1]
    print "Your process ID is: ", pro_id
    return pro_id
#______________________________________________________________________________#
def checkProcess ( objID ):
    """Takes an object Id and checks for process status. Will loop until process is complete."""

    valuzCheck= [
        ('cmdr','-qpRawCheck'),
        ('showreqs','0'),
        ('reqObjID', objID)
    ]
    comandCheck = urllib.urlencode(valuzCheck)
    stat = 0
    while stat <= 5:
        print "Progress report on object", objID
        response3 = opener.open(hive_URL, comandCheck)
        check = response3.read()
        stat = int(check.split('\n')[1].split(',')[6])
        prog = int(check.split('\n')[1].split(',')[8])
        if stat == 5: print "DONE!"; stat = 6; continue
        elif stat == 4: print "Process in Line"
        elif stat == 3: print "Process Running.", prog, "percent complete"
        elif stat == 2: print "Dont care"
        elif stat == 1: print "Process in submision"
        else: print "PROGRAM ERROR!!!!"; break 
        time.sleep(120)
#______________________________________________________________________________#
def getHitList ( objID, sample ):
    """Uses ObjID to retreive the service Hit List"""
    print "Getting Hit List from process...\n"

    valuzList =[
        ('cmdr','alCount'),
        ('objs',objID)
    ]

    comand     = urllib.urlencode(valuzList)
    response4  = opener.open(hive_URL, comand)
    hitListObj  = response4.read()
    hitList = sample+'.csv'
    with open(hitList, 'w') as hexHitLst:
        hexHitLst.write(hitListObj)
    print hitList, ' written to file'
#______________________________________________________________________________#
def archiveUAreads ( objID, sample ):
    """Uses ObjID to archive the read file"""
    print "Archiving reads...\n"
    readName = sample+'-contig.fa'
    valuzList =[
        ('cmdr','alFasta'),
        ('objs','objID'),
        ('found','0'),
        ('backend','1'),
        ('down','1'),
        ('arch','1'),
        ('arch_dstname', readName),
        ('cgi_dstname', readName),
        ('ext','fasta'),
        ('check','1'),
        ('raw','1'),
        ('bust','1501094999251')

    ]

    comand     = urllib.urlencode(valuzList)
    response4  = opener.open(hive_URL, comand)
    readObj  = response4.read()
    print readObj
    print readName, ' archived to db'
#______________________________________________________________________________#
def main ():
    response = logInHIVE (login,pwd)
    objDict = readIDlist(lstfile)
    for sample in objDict.keys()[:2]:
        print sample, objDict[sample][0]
        object_id = submitProcess(sample, objDict[sample][0], gutDB)
        checkProcess (object_id)
        archiveUAreads(object_id, sample)
        getHitList (object_id, sample)
#______________________________________________________________________________#
if __name__ == '__main__': main()