#!/usr/bin/env python
# -*- coding: utf-8 -*-

################################################################################
                            ##Size and Reads##
""""Reads JSON text file from HIVE"""
################################################################################
import os, json, csv

json_file = "/Users/hadley/BoxSync/Mazumdar_Lab/Gut/thesis/dataFiles/reads.dump.json"
genomes = {}
#______________________________________________________________________________#
def readJSON( file ):
    """loads a json file"""
    
    with open(file) as data_file:
        data = json.load(data_file)
    return data
#______________________________________________________________________________#
def write (list):
    """writes a json file"""
    order = list[0].keys()
    #print header
    for o in order: print o, ',',
    print '\r'
    for j in list:
        for o in order: print j[o], ',',
        print '\r'
    
#______________________________________________________________________________#
def main ():
    newList = []
    data = readJSON(json_file)
    write(data)

#______________________________________________________________________________#
if __name__ == '__main__': main()