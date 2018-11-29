#!/usr/bin/env python3.5
# -*- coding: utf-8 -*-

################################################################################
                            ##Microb KB Generation##
""""Generates a matrix for the microbe kb form different sites"""
################################################################################

import urllib, urllib2, re, csv
from bs4 import BeautifulSoup
from Bio import ExPASy, SeqIO, SwissProt, Entrez

Entrez.email= "hadley_king@gwmail.gwu.edu"
wiki_url    = 'https://microbewiki.kenyon.edu/index.php/'
prot_url    = 'http://www.uniprot.org/proteomes/?query=taxonomy:'
proteome    = 'http://www.uniprot.org/proteomes/'
nuccore_url = 'https://www.ncbi.nlm.nih.gov/nuccore/?term='
in_file     = '/Users/hadleyking/Desktop/fml/dataFiles/v1.4.csv'
out_file    = '/Users/hadleyking/Desktop/fml/scripts/test.csv'
microbe_db  = {}
prot_db     = {}
wiki_db     = {}
id_list     = []
mw_urls     = []
id_list     = []
PMIDs       = []
description = ''
citation    = ''
#______________________________________________________________________________#
def getGutDB ( file ):
    """reads the Gut DB accessions into a list for comparison"""

    gutDBList = []
    with open(file, 'rU') as read:
        reader = csv.reader(read)
        for cell in reader:
            gutDBList.append(cell[1])
    return gutDBList
#______________________________________________________________________________#
def acc2tax ( list ):
    """takes a list of accession numbers, calls NCBI and returns the TaxId, Name, and Lineage"""

    taxList = []
    for i in list:
        handle = Entrez.esummary(db ="nuccore", id = i)
        record = Entrez.read(handle)
        # if tax not in taxList:
        #     taxList.append(tax)
        taxList.append(record[0]['TaxId'])

#    print len(taxList)
    return taxList
#______________________________________________________________________________#
def tax2name( list ):
    """takes a list of TaxIds, calls NCBI and returns the name and lineage"""

    lineage, name = [], []
    for i in list:
        handle = Entrez.efetch(db ="taxonomy", id = i)
        record = Entrez.read(handle)
        lineage.append(record[0]['Lineage'])
        name.append(record[0]['ScientificName'])
    return lineage, name
#______________________________________________________________________________#
def pubMed ( list ):
    """Takes a tax Id list and returns a dict with PubMed entries"""
    
    entrez_db   = {}
    # for i in list:
    #     if i not in entrez_db.keys():
    #
    return entrez_db
#______________________________________________________________________________#
# def micWiki ():
#______________________________________________________________________________#
# def protDB ():
#______________________________________________________________________________#
def main ():
    gutDBList = getGutDB(in_file)
    print len(gutDBList), 'accessions'
    taxList = acc2tax(gutDBList)
    lineage, name = tax2name(taxList)
    with open(out_file, 'wb') as out:
        writer = csv.writer(out)
        for i in range(len(name)):
            writer.writerow([str(taxList[i]),\
            str(name[i]), str(lineage[i]),\
            str(gutDBList[i])])
 #   for i in range(len(taxList)):
 #        microbe_db[gutDBList[i]] = [taxList[i],name[i],lineage[i]]
 #    # entrez_db = pubMed(taxList)
 #    # for key, value in microbe_db.items():
 #    #     print key, microbe_db[key][0], microbe_db[key][1], microbe_db[key][2]
 #    with open('taxid.tsv', 'w') as file:
 #        for i in range(len(taxList)):
 #            out_line = str(gutDBList[i])\
 #                +'\t'+str(taxList[i])\
 #                +'\t'+str(name[i])\
 #                +'\t'+ str(lineage[i])+'\n'
 #            file.write(out_line)
 #    #    for i in taxList: print i
#______________________________________________________________________________#
if __name__ == '__main__': main()

