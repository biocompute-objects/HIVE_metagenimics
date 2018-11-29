#!/usr/bin/env python
# -*- coding: utf-8 -*-

################################################################################
                            ##...##
""""..."""
################################################################################
import csv
infile = "/Users/hadleyking/Downloads/fts.csv" #"/Users/hadleyking/Dropbox/SharedGut/raw_data/healthyMicroBiometaxDict_v1.3.csv"

#______________________________________________________________________________#
def getGutDB ( file ):
    """reads the Gut DB accessions into a list for comparison"""

    gutDBList_old = []
    gutDBList_new = []
    with open(file, 'rU') as read:
        reader = csv.reader(read)
        next(reader)
        for cell in reader:
            gutDBList_old.append(cell[0])
            gutDBList_new.append(cell[1])
    return gutDBList_old, gutDBList_new
#______________________________________________________________________________#
def compare ( list1, list2 ):
    """checks the content of one list against another. Unique items are added to a new list"""
    newList = []
    for i in list2:
        if i not in list1:
            newList.append(i)
    return newList
#______________________________________________________________________________#
def main ():
    gutList_old, gutList_new = getGutDB(infile)
    for i in gutList_old:
        if i not in gutList_new:
            print i
#______________________________________________________________________________#
if __name__ == '__main__': main()