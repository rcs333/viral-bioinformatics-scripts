
import glob
g = open('metadata_s1_large.csv', 'w')
count = 0
for name in glob.glob('S1*.fastq'):
	g.write(name + ',' + str(count) + '\n')
	count += 1
g.close()

count = 0
e = open('metadata_s2_large.csv', 'w')
for name in glob.glob('S2*.fastq'):
	e.write(name + ',' + str(count) + '\n')
	count += 1
e.close()
