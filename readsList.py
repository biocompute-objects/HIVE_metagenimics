#!/usr/bin/env python
# -*- coding: utf-8 -*-

################################################################################
                            ##JSON ID, HIVE##
""""JSON conversion of text file from HIVE"""
################################################################################
import os, json, csv

json_file = "/Users/hadleyking/Downloads/reads.json"
out = '/Users/hadleyking/Downloads/reads_ids.csv'
#______________________________________________________________________________#
def readJSON( file ):
    """loads a json file"""
    genomes = {}
    with open(file) as data_file:
        data = json.load(data_file)
    span = len(data)
    count = 0
    for i in data:
        name = i['name'].split('_')[0]
        print i["_id"], i['name']
    return genomes

#______________________________________________________________________________#
def main ():
    newList = []
    genomes = readJSON(json_file)
    print genomes.values()
    with open(out, 'w') as outfile:
        for i in genomes.keys():
            string = str(genomes[i])+','+str(i)+'\n'
            outfile.write(string)
#______________________________________________________________________________#
if __name__ == '__main__': main()