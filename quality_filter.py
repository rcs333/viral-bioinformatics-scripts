import subprocess
import glob

for name in glob.glob('*.fastq'):
	for qual in [37,38,39,40,41,42,43,44,45]:
		base = name.split('.')[0]
		# base = 's1-p0-mngs-0'
		out = '-'.join(base.split('-')[0:3]) + '-' + str(qual)
		subprocess.call('fastq_quality_filter -q ' + str(qual) + ' -p 100 -i ' + name + ' -o ' + out + '.fastq', shell=True)