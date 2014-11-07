#Wrapper for Wouter's replication of Zhang & Luck simultaneous arrays

epd scripts/ZLmat2csv.py data/raw data/csv  #may need to replace epd with your python
Rscript scripts/analyze.r data/csv          #analyze data
