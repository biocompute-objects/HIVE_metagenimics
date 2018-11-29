# HIVE metagenomics
Data Report:
1) Download a JSon of all read files
2) use [./scripts/sizeReads.py] to calculate the total number of reads and the total size of the reads

Read Processing:
1) Files downloaded from basespace
2) readfiles renamed using [./scripts/renameBaseSpace.py]
3) Reads uploaded to hive
4) The read files' metadata is exported to a JSON dump = [./reads.json]
5) Use [./scripts/readsList.py] to extract and map sample names and objIDs into a csv = [./reads_ids.csv]
6) Use [./scripts/list_censusHIVE.py] and [./reads_ids.csv] to submit each Censuscope process in order = [hadley_king@128.164.35.92/home/hadley_king/healthyGut/cen***.csv]
7) Use [./scripts/census.search.py], [./blackList.csv] and [./healthyMicroBiometaxDict.csv] to identify any potentially new organisms 
8) Add new organisms to the gutDB and re-version it.
	- compare old and new lists [./scripts/compare.py]
	- create new HiveSeq object with old db and new genomes. 
	- v1.3 = 175 accessions
	- v1.4 = 172 accessions
9) Run Hexagon on all samples
	- Use [./scripts/list_hexagonHIVE.py] and [./reads_ids.csv] to submit each Hexagon process in order = [hadley_king@128.164.35.92/home/hadley_king/healthyGut/hex***.csv]
10) use [./hexagonResults.py] create [./hexagonOutput.csv]
11) 

MicrobeDB:
1) take list of accessions and convert to taxid
2) 

# 3-23-17
1) get list
2) curate, check alignemnts
3) no plasmid/top level tax bc it skews results away  from a percise identification. 

Nutrition:
HMB:
1) Deleted columns A, C-R
2) replaced ids with the form ID_#_D#
3) Using [./nutritionCleaner.py], removed all daily entries above 4, outputting to [./cleanNutritionHMB.csv]
NNS: 
1) used [./makeGFKBsubjectNutrition.py] to make [./NNS_clean.csv]
	a) had to edit manually for some columns that were out of place:
		- Four blank columns were included in half the samples, and two date columns were included in sample 19 that had to be removed. 
	b) had to delete a few columns from the HMB data to make it match NNS, mostly blank columns or u"user entered" nutreients
2) used combined sheet to generate a 3-column table for GFKB using [./sqlNutrition.py]

**need to remove = JQ607428, CP002030, CP007180, LK931720, NR_103124, KF110997, NR_076809, NR_076999
