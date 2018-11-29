#!/usr/bin/env python
# -*- coding: utf-8 -*-

################################################################################
                            ##...##
""""..."""
################################################################################
import csv
taxfile = '/Users/hadleyking/Desktop/fml/dataFiles/hexagonOutput2.csv'
samplefile = '/Users/hadleyking/Desktop/fml/dataFiles/hexagonOutput1.csv'
outfile = '/Users/hadleyking/Desktop/fml/dataFiles/hexagonOutputTOT.csv'
taxDict = {}
accDict = {}
reader = csv.reader(open(taxfile, 'rU'))
for row in reader:
    taxDict[row[0]] = [row[1], row[2], row[3:]]
#print taxDict.keys()
reader = csv.reader(open(samplefile, 'rU'))
for row in reader:
    accDict[row[0]] = row[1:]
print accDict.keys()
with open(outfile, 'wb') as file:
    write = csv.writer(file)
    header = ['TaxId', 'SciName', 'Lineage', 'Accessions'] + accDict['Accession'][3:]
    print header
    write.writerow(header)
    nextheader = ['Unaligned', 'na', 'na'] + accDict['Unaligned']
    write.writerow(nextheader)
    for i in taxDict.keys():
#        print i, taxDict[i][2]
        if len(taxDict[i][2]) == 1:
            b = taxDict[i][2][0]
            taxDict[i] += accDict[b]
            line = [i] + taxDict[i]
            write.writerow(line)
        else: 
            for item in range(len(taxDict[i][2])):
                b = taxDict[i][2][item]
                line = taxDict[i] + accDict[b]
                line = [i] + line
                write.writerow(line)
file.close()