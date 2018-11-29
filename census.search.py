#!/usr/bin/env python
# -*- coding: utf-8 -*-

################################################################################
                            ##Accession Search##
""""Reads through the result files and populates dictionary with sample[accessionList] that are above detection threshhold """
################################################################################

#Declarations
import os, re, csv
my_dir = "/Users/hadleyking/Dropbox/SharedGut/raw_data/healthyMicroBiome/new/" 
term = "cen"
black_file = "/Users/hadleyking/Dropbox/SharedGut/Scripting/blackList.csv" 
gutDB = '/Users/hadleyking/Desktop/fml/dataFiles/v1.3.csv'
thresh = 5
fileList = []
sampleDict = {}

#______________________________________________________________________________#
def blacklistLoad( file ):
    """Loads black listed accessions to remove from results"""
    
    blackList  = []
    read   = csv.reader(open(file, "rU"))
    for row in read:
        if row[0] in blackList or row[0] == 'Accession' or row[0] == '':
             continue
        else: blackList += [row[0].split('.')[0]]
    return blackList;
#______________________________________________________________________________#
def createFileList(my_dir, term):
    """OS Walk to create file list based on a search term and a path"""
    
    for subdir, dirs, files in os.walk(my_dir):
        for file in files:
            if re.search(re.escape(term), file):
                result = os.path.join(subdir, file)
                fileList.append(result)
    return fileList
#______________________________________________________________________________#
def readCensusresultFile (file, dictionary, blacklist, threshold=10 ):
    """Takes an absolute file path, dictionary, a csv, and an optional threshold as input and returns a dictionary with taxId keys and accession number list as values"""
    sample = file.split('/')[-1].split('.')[0]
    with open (file, 'rU') as read:
        reader = csv.reader(read)
        for cell in reader:
            if cell[0] == '+': continue
            if cell[0] == '0': continue
            if cell[0] == 'id': continue
            cell[1] = cell[1].split('|')[3].split('.')[0]
            if int(cell[2]) >= threshold: 
                if cell[1] in blacklist: 
                    # print 'BLACKLISTED:', cell[1]
                    continue
#                print "got one"
                if dictionary.has_key(sample):
                    if cell[1] in dictionary[sample]: continue
                    else: dictionary[sample].append(cell[1])
                else: dictionary[sample] = [cell[1]]
    return dictionary
#______________________________________________________________________________#
def getGutDB ( file ):
    """reads the Gut DB accessions into a list for comparison"""

    gutDBList = []
    with open(file, 'rU') as read:
        reader = csv.reader(read)
        next(reader)
        for cell in reader:
            # print cell[1]
            gutDBList.append(cell[1])
    return gutDBList
#______________________________________________________________________________#
def compare ( dictionary, list ):
    """checks the content of a dictionary against a list. Unique items are added to a new list"""
    newList = []
    for key in dictionary.keys():
        # print len(sampleDict[key])
        for accession in dictionary[key]:
            # print accession,
            if accession not in list: 
                print accession, key
                if accession not in newList: newList.append(accession)
    return newList

#______________________________________________________________________________#
def main ():
    blackList = blacklistLoad(black_file)
    fileList = createFileList(my_dir, term)
    for i in fileList: 
        readCensusresultFile(i, sampleDict, blackList, thresh)
    gutDBList = getGutDB(gutDB)
    print len(gutDBList), 'gut orgs'
    newOrgs = compare(sampleDict, gutDBList)
    print len(newOrgs)
    for i in newOrgs: print i,
#______________________________________________________________________________#

if __name__ == '__main__': main()
