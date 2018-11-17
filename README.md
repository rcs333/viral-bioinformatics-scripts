# viral-bioinformatics-scripts
One happy home for all my random and one-off viral bioinformatics scrips 

For sensitive single nucleotide mutation analysis quality_filter.py will perform a bunch of trimming operations on fastq files. From my testing on our data you can basically just filter on a quality score of 41. I've been pairing and merging reads in geneious, running emit_metadata.py, then running lava with -save and running mut_count.py on the vcf files. Then I import the csv output into R to generate graphs. 
