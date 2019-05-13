import argparse
import sys
import glob


def up_count(s1, s2, c1, c2):
	global a_count
	global c_count
	global t_count
	global g_count

	global a_to_c
	global a_to_t
	global a_to_g 

	global c_to_a 
	global c_to_t
	global c_to_g

	global t_to_a
	global t_to_c 
	global t_to_g

	global g_to_a
	global g_to_c
	global g_to_t

	if s1 == 'A':
		a_count += c1
		if s2 == 'C':
			a_to_c += c2
		elif s2 == 'T':
			a_to_t += c2
		elif s2 == 'G':
			a_to_g += c2
	elif s1 == 'C':
		c_count += c1
		if s2 == 'A':
			c_to_a += c2
		elif s2 == 'T':
			c_to_t += c2
		elif s2 == 'G':
			c_to_g += c2
	elif s1 == 'T':
		t_count += c1
		if s2 == 'A':
			t_to_a += c2
		elif s2 == 'C':
			t_to_c += c2
		elif s2 == 'G':
			t_to_g += c2
	elif s1 == 'G':
		g_count += c1
		if s2 == 'A':
			g_to_a += c2
		elif s2 == 'C':
			g_to_c += c2
		elif s2 == 'T':
			g_to_t += c2





for filepath in glob.glob('*.fastq.vcf'):
	g = open(filepath + '.csv', 'w')
	print(filepath)
	for AF_CUTOFF in [0.05]:
		g_to_t = 0
		a_count = 0	
		c_count = 0
		t_count = 0
		g_count = 0

		a_to_c = 0
		a_to_t = 0
		a_to_g = 0

		c_to_a = 0
		c_to_t = 0
		c_to_g = 0

		t_to_a = 0
		t_to_c = 0
		t_to_g = 0

		g_to_a = 0
		g_to_c = 0
		g_to_t = 0

		for line in open(filepath):
			# not a comment at the header
			if line[0] !=  '#':
				line_split = line.split('\t')

				if len(line_split[3]) == 1 and len(line_split[4]) == 1:
					if int(line_split[1]) <= 50000 and int(line_split[1]) >= 0:
						if int(line_split[10].split(':')[3]) != 0:
							if float(line_split[10].split(':')[4]) / float(line_split[10].split(':')[3]) <= AF_CUTOFF:
								up_count(line_split[3], line_split[4], int(line_split[10].split(':')[3]), int(line_split[10].split(':')[4]))
								#print(line)
		total = a_count + c_count + t_count + g_count# + a_to_c + a_to_t + a_to_g + c_to_a + c_to_t + c_to_g + t_to_a + t_to_c + t_to_g + g_to_a + g_to_c + g_to_t
		print('Total Bases counted: ' + str(total))
		if total != 0:
			total = total / 10000.0
		else:
			total = 1

		print()
		print('A count: ' + str(a_count/total))
		print('\tA -> C: ' + str(a_to_c/total))
		print('\tA -> T: ' + str(a_to_t/total))
		print('\tA -> G: ' + str(a_to_g/total))
		print('')
		print('C count: ' + str(c_count/total))
		print('\tC -> A: ' + str(c_to_a/total))
		print('\tC -> T: ' + str(c_to_t/total))
		print('\tC -> G: ' + str(c_to_g/total))
		print('')
		print('T count: ' + str(t_count/total))
		print('\tT -> A: ' + str(t_to_a/total))
		print('\tT -> C: ' + str(t_to_c/total))
		print('\tT -> G: ' + str(t_to_g/total))
		print('')
		print('G count: ' + str(g_count/total))
		print('\tG -> A: ' + str(g_to_a/total))
		print('\tG -> C: ' + str(g_to_c/total))
		print('\tG -> T: ' + str(g_to_t/total))

		info = filepath.split('.')[0]
		print(info)
		samp = info.split('-')[0]
		con = ''
		prep = info.split('-')[1]
		qual_score = ''
		g.write(samp + ',' + prep + ',' + con + ',total,' + str(total) +','+ str(AF_CUTOFF)+ ',' + qual_score +'\n')

		g.write(samp + ',' + prep + ',' + con + ',A,' + str(a_count) +','+ str(AF_CUTOFF)+ ',' + qual_score +'\n')
		g.write(samp + ',' + prep + ',' + con + ',AC,' + str(a_to_c/total) +','+ str(AF_CUTOFF)+ ',' + qual_score +'\n')
		g.write(samp + ',' + prep + ',' + con + ',AT,' + str(a_to_t/total) + ','+ str(AF_CUTOFF)+ ',' + qual_score +'\n')
		g.write(samp + ',' + prep + ',' + con + ',AG,' + str(a_to_g/total) + ','+ str(AF_CUTOFF)+ ',' + qual_score +'\n')

		g.write(samp + ',' + prep + ',' + con + ',C,' + str(c_count) +','+ str(AF_CUTOFF)+ ',' + qual_score +'\n')
		g.write(samp + ',' + prep + ',' + con + ',CA,' + str(c_to_a/total) + ','+ str(AF_CUTOFF)+ ',' + qual_score +'\n')
		g.write(samp + ',' + prep + ',' + con + ',CT,' + str(c_to_t/total) + ','+ str(AF_CUTOFF)+ ',' + qual_score +'\n')
		g.write(samp + ',' + prep + ',' + con + ',CG,' + str(c_to_g/total) + ','+ str(AF_CUTOFF)+ ',' + qual_score +'\n')

		g.write(samp + ',' + prep + ',' + con + ',T,' + str(t_count) +','+ str(AF_CUTOFF)+ ',' + qual_score +'\n')
		g.write(samp + ',' + prep + ',' + con + ',TA,' + str(t_to_a/total) + ','+ str(AF_CUTOFF)+ ',' + qual_score +'\n')
		g.write(samp + ',' + prep + ',' + con + ',TC,' + str(t_to_c/total) +','+ str(AF_CUTOFF)+  ',' + qual_score +'\n')
		g.write(samp + ',' + prep + ',' + con + ',TG,' + str(t_to_g/total) + ','+ str(AF_CUTOFF)+ ',' + qual_score +'\n')

		g.write(samp + ',' + prep + ',' + con + ',G,' + str(g_count) +','+ str(AF_CUTOFF)+ ',' + qual_score +'\n')
		g.write(samp + ',' + prep + ',' + con + ',GA,' + str(g_to_a/total) + ','+ str(AF_CUTOFF)+ ',' + qual_score +'\n')
		g.write(samp + ',' + prep + ',' + con + ',GC,' + str(g_to_c/total) + ','+ str(AF_CUTOFF)+ ',' + qual_score +'\n')
		g.write(samp + ',' + prep + ',' + con + ',GT,' + str(g_to_t/total) + ','+ str(AF_CUTOFF)+ ',' + qual_score +'\n')
		g.close()
