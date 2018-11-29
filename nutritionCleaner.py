#!/usr/bin/env python
# -*- coding: utf-8 -*-

################################################################################
                            ##...##
""""..."""
################################################################################
import csv

infile = '/Users/hadleyking/Desktop/fml/dataFiles/nutrition/HMBDietDataCombined.csv'
outfile = '/Users/hadleyking/Desktop/fml/dataFiles/nutrition/cleanNutrition.csv'
writer = csv.writer(open(outfile, 'a'))
with open(infile, 'rU') as filein:
    reader = csv.reader(filein)
    for row in reader:
        if row[0] == 'Participant ID': 
            writer.writerow(row)
            continue
        if int(row[0].split('_')[-1].split('D')[1]) > 4: continue
        else: writer.writerow(row)