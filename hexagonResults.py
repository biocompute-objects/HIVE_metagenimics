#!/usr/bin/env python
# -*- coding: utf-8 -*-

################################################################################
                            ##Hexagon Results##
""""Reads through the hexagon result files and populates dictionary with ..."""
################################################################################

#Declarations
import urllib, urllib2, os, re, csv
from bs4 import BeautifulSoup
from Bio import ExPASy, SeqIO, SwissProt, Entrez
Entrez.email= "hadley_king@gwmail.gwu.edu"
my_dir = "/Users/hadleyking/Desktop/fml/dataFiles/hive/hex" 
term = "hex"
fileList = []
sampleDict = {}
outfile = '/Users/hadleyking/Desktop/fml/dataFiles/hexagonOutput.csv'
#______________________________________________________________________________#
def getFileList ( path, term ):
    """Takes a pathe and creats a file list with files to open"""

    file_list = []
    for subdir, dirs, files in os.walk(path):
        for file in files:
            if re.search(re.escape(term), file):
                result = os.path.join(subdir, file)
                file_list.append(result)
    return file_list
#______________________________________________________________________________#
def readHexagon ( list ):
    """checks the content of a list of files."""

    sampleDict = {}
    bugList = []
    bugList.append('Unaligned')
    for i in list:
        accDict = {}
        sample = i.split('/')[-1].split('.')[0]
        if sample.startswith('hexNNS'):
            sample = 'NNS_'+sample[5:]
        if sample.startswith('hexHMB'):
            sample = 'HMB_'+sample[5:]
        reader = csv.reader(open(i, 'rU'))
        reader.next()
        sampleDict[sample] = accDict
        for row in reader:
            if row[1] == 'total': continue
            if row[1] == 'Unaligned': 
                accDict[row[1]]=row[2]
                continue
            accession = row[1].split('|')[1].split('.')[0]
            if accession not in bugList: bugList.append(accession)
            accDict[accession]=row[2]
    return sampleDict, bugList
#______________________________________________________________________________#
def acc2tax ( value ):
    """takes an accession number, calls NCBI and returns the TaxId and Name"""
    taxId = ''
    if value == 'Unaligned': return ['na']
    else:
        handle = Entrez.esummary(db ="nuccore", id = value)
        record = Entrez.read(handle)
        taxId = record[0]['TaxId']
    return taxId
#______________________________________________________________________________#
def tax2Line( value ):
    """takes a list of TaxIds, calls NCBI and returns the name and lineage"""

    lineage = ['na']
    if value == ['na']: return 'na'
    else:
        taxId = value
        handle = Entrez.efetch(db ="taxonomy", id = taxId)
        record = Entrez.read(handle)
        lineage, name = record[0]['Lineage'], record[0]['ScientificName']
    return lineage, name
#______________________________________________________________________________#
def main ():
    file_list = getFileList(my_dir, term)
    samples, accessions = readHexagon(file_list)
    print len(accessions)
    # for s in samples.keys():
    #     print s
    # tax = {}
#     for a in accessions:
#         t = acc2tax(a)
#         l, n = tax2Line(t)
#         if t == ['na']: continue
#         if t not in tax.keys():
#             print t
#             tax[t] = [n, l, a]
#         else: tax[t] += [a]
#         print t, tax[t]
#     with open(outfile, 'wb') as file:
#         write = csv.writer(file)
#         header = ['TaxId', 'SciName', 'Lineage'] + samples.keys()
#
#         write.writerow(header)
#         for t in tax.keys():
#             line = [t]+tax[t][:2]
#             print line
#             for f in tax[t][2:]:
#                 for s in samples.keys():
#                     if f in samples[s]:
#                         try: line += [samples[s][f]]
#                         except: line += ['-']
#             print line
#             write.writerow(line)
#     file.close()
#______________________________________________________________________________#

if __name__ == '__main__': main()
