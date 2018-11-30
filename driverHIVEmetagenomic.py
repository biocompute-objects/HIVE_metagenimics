#!/usr/bin/env python3.5
# -*- coding: utf-8 -*-

################################################################################
                            ##censusHIVEwait##
""""Submit an instance of HIVE metagenomic pipeline"""
################################################################################
from cookielib import CookieJar
import urllib, urllib2, re, csv, requests, time, os, json, sys

black_file = "blackList-v2.0.csv"
hive_URL   = 'https://hive.biochemistry.gwu.edu/dna.cgi?'
sample     = raw_input('What is the sample name?\n')
query1     = raw_input('What is the read file Object ID?\n')
query2     = raw_input('If this is a paired read file enter the second ID now. \nOtherwise hit enter\n')
nt_db      = '513957'
logger     = './temp/'+sample+'_log.txt'
#______________________________________________________________________________#
def logIn(  ):
    """Login to HIVE, start session. Returns cookies for session"""

    login      = raw_input('Enter Log In:\n')
    os.system("stty -echo")
    pwd        = raw_input('Enter Password:')
    os.system("stty echo")
    cj         = CookieJar()
    opener     = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    log_in     = str('api=0&cmdr=login&login='+login+'&pswd='+pwd)
    response   = opener.open(hive_URL, log_in)
    print "You are logged in to the HIVE..."
    return opener;
#______________________________________________________________________________#
def blacklistLoad( file ):
    """Loads black listed accessions to remove from computations"""

    blackList  = []
    read   = csv.reader(open(file, "rU"))
    for row in read:
        if row[0] in blackList: continue
        if row[0] == 'Accession' : continue
        if row[0] == '': continue
        else: blackList += [row[0]]
    return blackList;
#______________________________________________________________________________#
def census( sample, query1, query2, nt_db ):
    """Submits the censuscope computation. Input is sample name, paired-end reads, and a db to align against. Returns the computation ID and the name"""

    print "Submitting CensuScope Process\n"
    censuName = sample+'_R'+str(iteration)
    valuzCensus = [
        ('cmdr','-qpProcSubmit'),
        ('svc','svc-dna-screening'),
        ('prop.svc-dna-screening.action','2'),
        ('prop.svc-dna-screening._type','svc-dna-screening'),
        ('prop.svc-dna-screening.alignSelector.21','svc-align-blast'),
        ('prop.svc-dna-screening.automanual.22','0'),
        ('prop.svc-dna-screening.batch_svc.5','single'),
        ('prop.svc-dna-screening.blastWordSize.29','28'),
        ('prop.svc-dna-screening.CensusIterations.6','1'),
        ('prop.svc-dna-screening.CensuslimitIterations.7','5'),
        ('prop.svc-dna-screening.chunk_size.9','4000'),
        ('prop.svc-dna-screening.cutOffvalue.11','0.0005'),
        ('prop.svc-dna-screening.filterNs.12','1'),
        ('prop.svc-dna-screening.isPostponed.20.3','0'),
        ('prop.svc-dna-screening.name.1',censuName),
        ('prop.svc-dna-screening.query.1.1',query1),
        ('prop.svc-dna-screening.query.1.23',query2),
        ('prop.svc-dna-screening.reqPriority.20.7','0'),
        ('prop.svc-dna-screening.resultInQueryDir.26','0'),
        ('prop.svc-dna-screening.Sample.15','2500'),
        ('prop.svc-dna-screening.scissors.16','hiveseq'),
        ('prop.svc-dna-screening.selfStopping.27','0'),
        ('prop.svc-dna-screening.slice.17','0'),
        ('prop.svc-dna-screening.split.18','-'),
        ('prop.svc-dna-screening.storeAlignments.28','1'),
        ('prop.svc-dna-screening.subject',nt_db),
        ('prop.svc-dna-screening.submitter.33','dna-screening'),
        ('prop.svc-dna-screening.svc','dna-screening'),
        ('prop.svc-dna-screening.svcTitle','CensuScope'),
        ('prop.svc-dna-screening.systemVersion.20.11','1.1'),
        ('prop.svc-dna-screening.taxDepth.25','leaf'),
        ('prop.svc-dna-screening.textBasedColumn.31.1','0'),
        ('prop.svc-dna-screening.textBasedFileSeparator.31.2','1')
    ]
    
    comandCensus = urllib.urlencode(valuzCensus)
    print comandCensus
    response2 = opener.open(hive_URL, comandCensus)
    census_id = response2.read()
    census_id = census_id.split(',')[1]
    print "Your CensuScope ID is: ",census_id
    return census_id, censuName; 
#______________________________________________________________________________#
def checkComputation( compID ):
    """Checks for cmpletion of computation. Takes the Obj ID as input and holds script untill computation is complete"""

    valuzCheck = [
        ('cmdr','-qpRawCheck'),
        ('showreqs','0'),
        ('reqObjID',compID)
    ]

    comandCheck = urllib.urlencode(valuzCheck)
    stat = 0
    while stat <= 5:
        print "Progress report on object", compID
        response3 = opener.open(hive_URL, comandCheck)
        check = response3.read()
        stat = int(check.split('\n')[1].split(',')[6])
        prog = int(check.split('\n')[1].split(',')[8])
        if stat == 5: print "DONE!"; stat = 6; continue
        elif stat == 4: print "Process in Line"
        elif stat == 3: print "Process Running.", prog, "percent complete"
        elif stat == 2: print "Dont care"
        elif stat == 1: print "Process in submision"
        else: print "PROGRAM ERROR!!!! Unidentified Status Code"; break 
        time.sleep(30)
    return;
#______________________________________________________________________________#
def censusHitList( compID, censuName, blackList ):
    """Downloads the hitlist result file and creates the HIVE Seq list. Input is object ID, Name, and blacklist. Returns list of indices for the HiveSeq Obj"""

    print "Getting Hit List from CensuScope...\n"

    valuzCensusList =[
        ('cmdr','alCount'),
        ('objs',compID)
    ]

    comand     = urllib.urlencode(valuzCensusList)
    response4  = opener.open(hive_URL, comand)
    censusHit  = response4.read()
    hitListCen = 'cen'+census_id+'_'+censuName+'.csv'
    with open(hitListCen, 'w') as cenHitLst:
        cenHitLst.write(censusHit)
    print hitListCen, ' written to file'
    lines      = censusHit.split('\n')
    hiveseqQry = ''
    for i in lines[1:]:
        try : 
            hits = int(i.split('|')[-1].split(',')[-3])
            acc = i.split('|')[3]
            index = i.split(',')[0]
            if hits >= 10: 
                if acc in blackList:
                    print acc, " is black Listed", hits
                else :
                    print index, hits, acc
                    seq_index = nt_db+','+index+','+index+';'
                    hiveseqQry+=(seq_index)
            else: continue
        except: continue
    hiveseqQry = hiveseqQry[0:-1]
    return hiveseqQry;
#______________________________________________________________________________#
def hiveSeqObj( hiveseqQry ):
    """Creates a HiveSeq Object. Input is a index list of sequences. Returns a HiveSeq Archiver ID"""

    print "Creating Hive Seq Obj\n"
    hiveSeqName = sample+'HiveSeq'+'_R'+str(iteration)
    hiveSeq_valuz = [
        ('cmdr','-qpProcSubmit'),
        ('svc','dna-hiveseq'),
        ('raw','1'),
        ('prop.svc-hiveseq.name.1',hiveSeqName),
        ('prop.svc-hiveseq.AlgorithmsName.11.0','0'),
        ('prop.svc-hiveseq.lowcomplexityactive.12.0','0'),
        ('prop.svc-hiveseq.lowcomplexityWindow.12.0','15'),
        ('prop.svc-hiveseq.lowcomplexityEntropy.12.0','1'),
        ('prop.svc-hiveseq.lowcomplexityOption.12.0','0'),
        ('prop.svc-hiveseq.AdaptersFilter.13','0'),
        ('prop.svc-hiveseq.adaptersactive.13.0','0'),
        ('prop.svc-hiveseq.adaptersObjId.13.0','0'),
        ('prop.svc-hiveseq.adaptersReverse.13.0.0','0'),
        ('prop.svc-hiveseq.adaptersComplement.13.0.1','0'),
        ('prop.svc-hiveseq.adaptersMaxmissmatches.13.0','2'),
        ('prop.svc-hiveseq.adaptersMinLength.13.0','10'),
        ('prop.svc-hiveseq.primersactive.17.0','0'),
        ('prop.svc-hiveseq.primersReverse.17.0.0','0'),
        ('prop.svc-hiveseq.primersComplement.17.0.1','0'),
        ('prop.svc-hiveseq.primersKeep.17.0','0'),
        ('prop.svc-hiveseq.primersMaxmissmatches.17.0','2'),
        ('prop.svc-hiveseq.primersMinLength.17.0','100'),
        ('prop.svc-hiveseq.QualityFilter.19','0'),
        ('prop.svc-hiveseq.qualityactive.19.0','0'),
        ('prop.svc-hiveseq.qualityPercentage.19.0','100'),
        ('prop.svc-hiveseq.qualityThreshold.19.0','50'),
        ('prop.svc-hiveseq.trimMinimum.20.0','-1'),
        ('prop.svc-hiveseq.trimMaximum.20.0','-1'),
        ('prop.svc-hiveseq.removeMin.21.0.0','-1'),
        ('prop.svc-hiveseq.removeMax.21.0.0','-1'),
        ('prop.svc-hiveseq.lengthSeqFilter.16','0'),
        ('prop.svc-hiveseq.minimumSeqLength.16.0','0'),
        ('prop.svc-hiveseq.idfilteractive.15.0','0'),
        ('prop.svc-hiveseq.idlistObjId.15.0','0'),
        ('prop.svc-hiveseq.listExclusion.15.0','0'),
        ('prop.svc-hiveseq.randomizerNumValue.22.0','100'),
        ('prop.svc-hiveseq.randomizerNoise.22.1','0'),
        ('prop.svc-hiveseq.randomizerMinLength.22.2','100'),
        ('prop.svc-hiveseq.randomizerMaxLength.22.3','100'),
        ('prop.svc-hiveseq.randomizerRevComp.22.6','0'),
        ('prop.svc-hiveseq.randLengthNorm.22.7','1'),
        ('prop.svc-hiveseq.seqExclusionOption.23.1','0'),
        ('prop.svc-hiveseq.seqExclusionRevComp.23.2','0'),
        ('prop.svc-hiveseq.hiveseqQry.24',hiveseqQry),
        ('prop.svc-hiveseq.inputMode.25','0'),
        ('prop.svc-hiveseq.pecPairEndFile.18.0','0'),
        ('prop.svc-hiveseq.pecMinMatchLen.18.0','15'),
        ('prop.svc-hiveseq.pecQualities.18.0','1'),
        ('prop.svc-hiveseq.pecKeepAlignments.18.0','0'),
        ('prop.svc-hiveseq.denovoExtSizemer.14.0','16'),
        ('prop.svc-hiveseq.denovoExtSizeFilter.14.0','0'),
        ('prop.svc-hiveseq.denovoExtRptFilter.14.0','0'),
        ('prop.svc-hiveseq.denovoExtFirstStage.14.0','1'),
        ('prop.svc-hiveseq.denovoOutFilterLength.14.0','1000'),
        ('prop.svc-hiveseq.denovoMissmatchesPercentage.14.0','2'),
        ('prop.svc-hiveseq.maxNumberQueryForHiveseq.25','-1'),
        ('prop.svc-hiveseq.inputMode.27.0','1'), #
        ('prop.svc-hiveseq.isFastQFile.26.0','1'),
        ('prop.svc-hiveseq.keepOriginalID.26.1','1'),
        ('prop.svc-hiveseq.appendLength.26.2','1'),
        ('prop.svc-hiveseq.isHiveseq.26.3','0'),
        ('prop.svc-hiveseq.isRevComp.26.4','0'),
        ('prop.svc-hiveseq.submitter.29','dna-hiveseq'),
        ('prop.svc-hiveseq._type','svc-hiveseq'),
        ('prop.svc-hiveseq.parent_proc_ids.9','3101923'),
        ('prop.svc-hiveseq.action.10.0','2'),
        ('prop.svc-hiveseq.isPostponed.10.3','0'),
        ('prop.svc-hiveseq.reqPriority.10.7','0')
    ]

    seq_comand = urllib.urlencode(hiveSeq_valuz)
    print seq_comand
    response5 = opener.open(hive_URL, seq_comand)

    hiveSeqMan = response5.read()
    hiveSeqMan = hiveSeqMan.split(',')[1]
    return hiveSeqMan;
#______________________________________________________________________________#
def hiveSeq_Id( hiveSeqMan ):
    """Takes the Archiver ID and returns the object id for the HiveSeq Obj"""

    prop_val = 'archiver/'+hiveSeqMan 

    hiveSeqMan_valuz = [
        ('cmdr','objList'),
        ('mode','json'),
        ('prop_val',prop_val),
        ('prop_name','base_tag')
    ]

    hiveSeqMan_comand = urllib.urlencode(hiveSeqMan_valuz)
    response2 = opener.open(hive_URL, hiveSeqMan_comand)
    hivSeqJSON = json.loads(response2.read())
    hiveSeqId = hivSeqJSON['objs']['_id']
    print "Your HiveSeq ID is: ", hiveSeqId
    return hiveSeqId;
#______________________________________________________________________________#
def hexagon( query1, query2, hiveSeqId ):
    """Submits a Hexagon computation. Inputs are read file/s IDs and a HiveSeq ID"""

    print "Creating Hexagon Alignment Object\n" 
    hexagonName = sample+'_R'+str(iteration)
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
        ('prop.svc-align-hexagon.seed.6.3','11'),
        ('prop.svc-align-hexagon.allowShorterEnds.6.0','0'),
        ('prop.svc-align-hexagon.maxNumberQuery.24','all'),
        ('prop.svc-align-hexagon.scissors.28','hiveseq'),
        ('prop.svc-align-hexagon.complexityRefEntropy.3.0.0','1.2'),
        ('prop.svc-align-hexagon.complexityRefWindow.3.0.0','30'),
        ('prop.svc-align-hexagon.complexityEntropy.3.1.0','1.2'),
        ('prop.svc-align-hexagon.complexityWindow.3.1.0','30'),
        ('prop.svc-align-hexagon.keepAllMatches.33','3'),
        ('2prop.svc-align-hexagon.maxHitsPerRead.23','200'),
        ('prop.svc-align-hexagon.minMatchLen.25','45'),
        ('prop.svc-align-hexagon.maxMissQueryPercent.2.0','15'),
        ('prop.svc-align-hexagon.considerGoodSubalignments.2.0','1'),
        ('prop.svc-align-hexagon.slice.15','500000'),
        ('prop.svc-align-hexagon._type','svc-align-hexagon'),
        ('prop.svc-align-hexagon.subject.16',hiveSeqId),
        ('prop.svc-align-hexagon.scoreFilter.21','None'),
        ('prop.svc-align-hexagon.action.0.0','2'),
        ('prop.svc-align-hexagon.doubleHash.20','0'),
        ('prop.svc-align-hexagon.doubleStagePerfect.30','1'),
        ('prop.svc-align-hexagon.split.17','query')
    ]

    hexagon_comand = urllib.urlencode(hexagon_valuz)
    print hexagon_comand
    response7 = opener.open(hive_URL, hexagon_comand)
    hex_id = response7.read()
    hex_id = hex_id.split(',')[1]
    print "Your Hexagon ID is: ", hex_id
    return hex_id, hexagonName
#______________________________________________________________________________#
def hexagonHitList( hex_id, hexagonName ):
    """Returns a Hexagon hitlist file"""

    print "Getting Hit List from Hexagon...\n"
    valuzHexHits = [
        ('cmdr','alCount'),
        ('objs',hex_id)
    ]
    comandHexHits = urllib.urlencode(valuzHexHits)
    response9 = opener.open(hive_URL, comandHexHits)
    hexHits = response9.read()
    hitListHex = 'hex'+hex_id+'_'+hexagonName+'.csv'
    with open(hitListHex, 'w') as hitLst:
        hitLst.write(hexHits)
    print hitListHex, ' written to file'
    return;
#______________________________________________________________________________#
def uaReadsArchiver(hex_id, sample, iteration):
    """Archives the unaligned reads from a Hexagon computation. Input is the Obj ID, sampel name, and iteration. Returns the object ID, object name, and archiver id"""

    print "Archiving unaligned reads from Hexagon...\n"
    #uaName = datetime.now().time()
    #uaName = str(name).split('.')[1]+'.fastq'
    uaName = 'UnalignedReads-'+hex_id+'_'+sample+'_R'+str(iteration)+'.fastq'
    unAligned_valuz = [
        ('cmd','alFastq'),
        ('objs',hex_id),
        ('found','0'),
        ('backend','1'),
        ('down','1'),
        ('arch','1'),
        ('arch_dstname',uaName),
        ('ext','fastq'),
        ('check','1'),
        ('raw','1'),
        ('bust','1475555936101')
    ]

    unAligned_comand = urllib.urlencode(unAligned_valuz)
    response10 = opener.open(hive_URL, unAligned_comand)
    print "Waiting for unaligned reads from Hexagon...\n"
    status = '1'
    while status == '1':
        time.sleep(10)
        print "checking for obj id"
        valuz = [
            ('cmdr','objList'),
            ('type','^nuc-read$'),
        #    ('reqObjID',hive_id),
            ('search',uaName),
            ('prop','name'),
            ('bust','1476369456692')
        ]

        comand = urllib.urlencode(valuz)
        print comand
        response2 = opener.open(hive_URL, comand)
        data = response2.read()
        try:
            uaID = data.split('.')[1]
            print uaID, ' processing'
            status = '0'
        except:
            print "Waiting..."
            status = '1'
            
    print "Retrieving svc-archiver obj ID to check on archival process"
    status = '1'
    while status == '1':
        time.sleep(10)
        print "Waiting for obj id to be gererated..."
        valuz = [
            ('cmdr','objList'),
            ('type','svc-archiver'),
        #    ('reqObjID',hive_id),
            ('search',uaName),
            ('prop','name'),
            ('bust','1476369456492')
        ]
        comand = urllib.urlencode(valuz)
        print comand
        response2 = opener.open(hive_URL, comand)
        data = response2.read()
        try:
            archID = data.split('.')[1]
            print archID, uaName
            status = '0'
        except:
            print
            status = '1'
    return uaID, uaName, archID 
#______________________________________________________________________________#
opener = logIn()
blackList = blacklistLoad(black_file)
iteration = 0
sys.stdout = open(logger, "a")
while iteration < 3:
    if iteration >= 1: query1, query2 = uaID, ''
    iteration += 1
    census_values = census(sample, query1, query2, nt_db)
    census_id, censuName = census_values[0], census_values[1]
    checkComputation(census_id)
    hiveseqQry = censusHitList(census_id, censuName, blackList)
    print hiveseqQry
    hiveSeqMan = hiveSeqObj(hiveseqQry)
    checkComputation(hiveSeqMan)
    hiveSeqId = hiveSeq_Id(hiveSeqMan)
    hexagon_valus = hexagon(query1, query2, hiveSeqId)
    hex_id, hexagonName = hexagon_valus[0], hexagon_valus[1]
    checkComputation(hex_id)
    hexagonHitList(hex_id, hexagonName)
    ua_valus = uaReadsArchiver(hex_id, sample, iteration)
    uaID, uaName, archID = ua_valus[0], ua_valus[1], ua_valus[2]
    checkComputation(archID)
print "Entire Pipe complete!"
