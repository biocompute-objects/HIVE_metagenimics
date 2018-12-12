# HIVE metagenomics Pipeline
This repository is based on computations using the [FDA HIVE](https://github.com/FDA/fda-hive) platform. 
>The High-performance Integrated Virtual Environment (HIVE), is a modern robust suite of software that provides an infrastructure for next-generation sequence (NGS) data analysis co-developed by Food and Drug Administration and George Washington University. The HIVE provides a distributed data retrieval system, archival capabilities, and computational environment architected to manipulate NGS data.

We use a two-step pipeline for this metagenomic analysis; [CensuScope](http://www.ncbi.nlm.nih.gov/pubmed/25336203) and [HIVE-hexagon](http://www.ncbi.nlm.nih.gov/pubmed/24918764). CensuScope is a census-based tool that randomly samples a user-defined number of reads and BLASTs them against a reference DB. Our reference database (a [filtered version of NTdb](https://hive.biochemistry.gwu.edu/filterednt)) is the NCBI Nucleotide db with all of the sequences lacking a clear taxonomic lineage filtered out. All artificial sequences have been removed either by our automated filter or manually, once an artificial sequence is identified during post analysis processing Sequences identified by CensuScope are used as references in Hexagon alignments. HIVE-hexagon, a K-mer based aligner, is more sensitive and faster than current standard alignment algorithms. HIVE-hexagon offers a decrease in computational cost, memory requirement and time for processing. For a full description of these methods please see [Baseline human gut microbiota profile in healthy people and standard reporting template](https://doi.org/10.1101/445353)

## Table of Contents:
* [BLAST Type Definition](prop-spec-blast.txt)
* [Blacklisted Accessions](blackList-v2.0.csv)
* [Hexagon Type Definition](def.svc-align-hexagon.json)
* [CensuScope Type Definition](def.svc-dna-screening.json)
* [Python script](driverHIVEmetagenomic.py)
* [HIVE_metagenomics BioCompute Object](HIVE_metagenomics.json)
* [Log File for BCO](HMB25-2_log.txt)
* [list of samples and object IDs](meta.csv)
* [Output of `stat` on `HMB25-2_log.txt`](stat_HMB25-2_log.txt)