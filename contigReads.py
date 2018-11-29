#!/usr/bin/env python
# -*- coding: utf-8 -*-

################################################################################
                            ##Size and Reads##
""""Reads JSON text file from HIVE"""
################################################################################
import os, json, csv

json_file = "/Users/hadleyking/Downloads/contigs.json"
#______________________________________________________________________________#
def readJSON( file ):
    """loads a json file"""
    samples = []
    with open(file) as data_file:
        data = json.load(data_file)
    span = len(data)
    print span
    for i in data:
        name, obj = i['name'], i['_id']
        print name, obj
        if name not in samples:
            samples.append(name) 
        else: print 'Dup', name
    return data

#______________________________________________________________________________#
def main ():
    newList = []
    genomes = readJSON(json_file)
#______________________________________________________________________________#
if __name__ == '__main__': main()