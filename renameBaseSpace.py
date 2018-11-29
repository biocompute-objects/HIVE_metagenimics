#!/usr/bin/env python
# -*- coding: utf-8 -*-

################################################################################
                            ##renameBaseSpace##
""""Searches for read files and renames them according to the mapping below"""
################################################################################
import glob, os, re

#Tuple list mapping names (new, old)
x = [("HMB2-1", "GW-97"), ("HMB2-2", "GW-98"), ("HMB2-3", "GW-99"), ("HMB3-1", "GW-100"), ("HMB3-2", "GW-101"), ("HMB3-3", "GW-102"), ("HMB4-1", "GW-103"), ("HMB4-2", "GW-104"), ("HMB4-3", "GW-105"), ("HMB10-1", "GW-106"), ("HMB10-2", "GW-107"), ("HMB10-3", "GW-108"), ("HMB11-1", "GW-109"), ("HMB11-2", "GW-110"), ("HMB11-3", "GW-111"), ("HMB12-1", "GW-112"), ("HMB12-2", "GW-113"), ("HMB12-3", "GW-114"), ("HMB13-1", "GW-115"), ("HMB13-2", "GW-116"), ("HMB13-3", "GW-117"), ("HMB19-1", "GW-118"), ("HMB19-2", "GW-119"), ("HMB19-3", "GW-120")] 

file_list = glob.glob('/Users/hadleyking/BaseSpace/GW_BATCH_6-35397370/*/*.fastq.gz')

my_dir = '/Users/hadleyking/BaseSpace/GW_BATCH_6-35397370/'

for subdir, dirs, files in os.walk(my_dir):
    for file in files:
# iterate through list of tuples
        for e in x:
            if re.search(re.escape(e[1]), file): 
                result = os.path.join(subdir, file)
                new_reads = my_dir+re.sub(e[1], e[0], file)
                os.rename(result, new_reads)
                print new_reads
