#!/usr/bin/env python
# -*- coding: utf-8 -*-

################################################################################
                            ## Read Hexagon All ##
"""Reads a directory containing Hexagon output files in the form of 
HiveID_Sample_R#.csv and writes to an output file."""
################################################################################

import csv, re, os
from Bio import Entrez
matchCnt, matchCnt_pct, id_list = [], [], []
Entrez.email = 'tud13145@temple.edu'
path = raw_input("What is the path you would like to analyze? \n")
path = path.rstrip()
search = "hex"
for d in os.listdir(path):
    if re.search(re.escape(search), d):
        result = path+"/"+d
        sample = d #raw_input("What is the smaple that you are analzing? \n")
        sample =  sample.split('_')
        iteration = str(sample[-1])
        iteration = iteration[1]
        ua_version, version = "", ""
        read = csv.reader(open(result, "rU"))
        print sample
        c = csv.writer(open(path+"/"+sample[1]+"_output.csv", "a"))
        c.writerow(["", "Hexagon Sample: ", sample[1]+"-R"+iteration])
        c.writerow(["Accession", "Leaf TaxId","Species", "Hits", "Percent", "Leaf GI"])
        next(read)
        for cell in read:
            if cell[1] == "Unaligned":  unaligned = int(cell[2])
            elif cell[0] == "+":        total_aligned = int(cell[2])
            else:                       continue
        
        if iteration == "1":    version, ua_version = "TR", "1st"
        elif iteration == "2":  ua_version = "2nd"
        else:                   ua_version = "3rd" 
       
        print "Calling NCBI..."
        total = total_aligned + unaligned
        total= str(total) 
        ua_percent = float(unaligned)/float(total)*100
        c.writerow(["",ua_version,"Unaligned Reads", unaligned, ua_percent]) 
        read1 = csv.reader(open(result, "rU"))
        next(read1) 

        for cell in read1:
            if cell[1] == "Unaligned" or cell[0] == "+":  continue

            else:        
                hits = cell[2]
                gb = cell[1]
                info = gb.split('|')
                i = info[3]
                handle = Entrez.esummary(db ="nucleotide", id = i)
                record = Entrez.read(handle)
                tax = record[0]['TaxId']
                percent = (float(hits)/float(total))*100
                c.writerow([info[1],tax, info[4], hits,percent, info[3]])
        c.writerow(["",version, "Total number of reads in sample: ", total])

        print d+" Done!"