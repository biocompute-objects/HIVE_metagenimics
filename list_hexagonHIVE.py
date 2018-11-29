#!/usr/bin/env python3.5
# -*- coding: utf-8 -*-

################################################################################
                            ##list_hexagonHIVE##
""""Submit a CensuScopr Job and waits for completion before submitting the next one in a list"""
################################################################################

from cookielib import CookieJar
import urllib, urllib2, re, csv, requests, time, os, json


login      = 'hadley_king@gwmail.gwu.edu'
os.system("stty -echo")
pwd        = 'T3mpl3Gr@d17'#raw_input('Enter Password:')
os.system("stty echo")
lstfile = '/Users/hadleyking/Desktop/fml/dataFiles/reads_ids1.csv'
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
def submitHexagon ( sample, query1, query2, nt_db ):
    """Submits the API request for a Hexagon computation"""
    print "Creating Hexagon Alignment Object\n" 
    hexagonName = sample
    hexagon_valuz = [
        ('cmdr','-qpProcSubmit'),
        ('svc','dna-hexagon'),
        ('raw','1'),
        ('prop.svc-align-hexagon.alignSelector.9','svc-align-hexagon'),
        ('prop.svc-align-hexagon.name.11',hexagonName),
        ('prop.svc-align-hexagon.query.1',query1),
        ('prop.svc-align-hexagon.query.1.23',query2),
        ('prop.svc-align-hexagon.submitter.14','dna-hexagon'),
        ('prop.svc-align-hexagon.isbackward.7.11','1'),
        ('prop.svc-align-hexagon.isextendtails.7.12','0'),
        ('prop.svc-align-hexagon.maxExtensionGaps.7.13','0'),
        ('prop.svc-align-hexagon.reverseEngine.7.3','0'),
        ('prop.svc-align-hexagon.isoptimize.7.6','1'),
        ('prop.svc-align-hexagon.hashStp.7.7','auto'),
        ('prop.svc-align-hexagon.hashCompileStp.7.8','auto'),
        ('prop.svc-align-hexagon.looseExtenderMinimumLengthPercent.7.0','66'),
        ('prop.svc-align-hexagon.looseExtenderMismatchesPercent.7.4','25'),
        ('prop.svc-align-hexagon.alignmentEngine.7.9','1'),
        ('prop.svc-align-hexagon.maxHashBin.7.2','50'),
        ('prop.svc-align-hexagon.selfQueryPosJumpInNonPerfectAlignment.7.1','1'),
        ('prop.svc-align-hexagon.useRedundSim.7.5','1'),
        ('prop.svc-align-hexagon.computeDiagonalWidth.7.10','auto'),
        ('prop.svc-align-hexagon.searchRepeatsAndTrans.5.0','0'),
        ('prop.svc-align-hexagon.isglobal.6.7','0'),
        ('prop.svc-align-hexagon.costGapNext.6.5','-4'),
        ('prop.svc-align-hexagon.costGapOpen.6.4','-12'),
        ('prop.svc-align-hexagon.costMatch.6.6','5'),
        ('prop.svc-align-hexagon.costMismatchNext.6.2','-6'),
        ('prop.svc-align-hexagon.costMismatch.6.1','-4'),
        ('prop.svc-align-hexagon.seed.6.3','14'),
        ('prop.svc-align-hexagon.allowShorterEnds.6.0','0'),
        ('prop.svc-align-hexagon.maxNumberQuery.24','all'),
        ('prop.svc-align-hexagon.scissors.28','hiveseq'),
        ('prop.svc-align-hexagon.complexityRefEntropy.3.0.0','1.2'),
        ('prop.svc-align-hexagon.complexityRefWindow.3.0.0','30'),
        ('prop.svc-align-hexagon.complexityEntropy.3.1.0','1.2'),
        ('prop.svc-align-hexagon.complexityWindow.3.1.0','30'),
        ('prop.svc-align-hexagon.keepAllMatches.33','3'),
        ('prop.svc-align-hexagon.maxHitsPerRead.23','10'),
        ('prop.svc-align-hexagon.minMatchLen.25','65'),
        ('prop.svc-align-hexagon.maxMissQueryPercent.2.0','10'),
        ('prop.svc-align-hexagon.considerGoodSubalignments.2.0','0'),
        ('prop.svc-align-hexagon.slice.15','500000'),
        ('prop.svc-align-hexagon._type','svc-align-hexagon'),
        ('prop.svc-align-hexagon.subject.16',nt_db),
        ('prop.svc-align-hexagon.scoreFilter.21','None'),
        ('prop.svc-align-hexagon.action.0.0','2'),
        ('prop.svc-align-hexagon.doubleHash.20','0'),
        ('prop.svc-align-hexagon.doubleStagePerfect.30','1'),
        ('prop.svc-align-hexagon.split.17','query'),
        ('prop.svc-align-hexagon.resolveConfictsUnique.13.1', '1'),
        ('prop.svc-align-hexagon.resolveConflicts.13.2', '2'),
        ('prop.svc-align-hexagon.resolveConflictsScore.13.3', '2')
    ]

    hexagon_comand = urllib.urlencode(hexagon_valuz)
    print hexagon_comand
    response7 = opener.open(hive_URL, hexagon_comand)
    hex_id = response7.read()
    hex_id = hex_id.split(',')[1]
    print "Your Hexagon ID is: ", hex_id
    return hex_id
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
    """Uses ObjID to retreive the Census Hit List"""
    print "Getting Hit List from CensuScope...\n"

    valuzList =[
        ('cmdr','alCount'),
        ('objs',objID)
    ]

    comand     = urllib.urlencode(valuzList)
    response4  = opener.open(hive_URL, comand)
    hitListObj  = response4.read()
    hitList = 'hex'+sample+'.csv'
    with open(hitList, 'w') as hexHitLst:
        hexHitLst.write(hitListObj)
    print hitList, ' written to file'
#______________________________________________________________________________#
def main ():
    response = logInHIVE (login,pwd)
    objDict = readIDlist(lstfile)
    for sample in objDict.keys():
        print sample, objDict[sample][1], objDict[sample][0]
    object_id = submitHexagon(sample, objDict[sample][1], objDict[sample][0], gutDB)
    checkProcess (object_id)
    getHitList (object_id, sample)
#______________________________________________________________________________#
if __name__ == '__main__': main()