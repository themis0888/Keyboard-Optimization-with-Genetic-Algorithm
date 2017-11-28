from collections import Counter
from os import walk
from config import CONFIG


'''
preprocess : string(file name) -> dict(for char), dict(for seq)
dict : set of {(string) : float}
Example : preprocess()
Eat the name of textfile(as a string) and calculate the frequency
of each aphabet and every sequence. 
'''

def Preprocess(filename = 'text.txt'):

	f = open(filename, 'r')
	chr_list = []
	lines = f.read()
	line_lst = list(lines.lower())
	for c in line_lst:
		if c.isalpha():
			chr_list.append(c)
	rel_list = []
	for i in range(len(chr_list)-1):
		rel_list.append(chr_list[i]+chr_list[i+1])
	alp_freq = Counter(chr_list)
	seq_freq = Counter(rel_list)

	return alp_freq, seq_freq, len(chr_list), len(rel_list)


alp_freq, seq_freq = dict(), dict()
for c in CONFIG['alphabet_string']:
	alp_freq[c] = 0
	for cc in CONFIG['alphabet_string']:
		seq_freq[c+cc] = 0

total_alp, total_seq = 0, 0

f = []
for (dirpath, dirnames, filenames) in walk('COCA/'):
	f.extend(filenames)

for name in filenames:
	temp_alp, temp_seq, num_alp, num_seq = Preprocess('COCA/'+ name)
	total_alp += num_alp
	total_seq += num_seq

	for i in temp_alp:
		alp_freq[i] += temp_alp[i]

	for i in temp_seq:
		seq_freq[i] += temp_seq[i]


for i in alp_freq:
	alp_freq[i] /= total_alp
for i in seq_freq:
	seq_freq[i] /= total_seq


fr = open('corpus_data.py','w')
fr.write('Alpha_freq = { \n')
for c in alp_freq:
	fr.write('\t\'' + str(c) + '\': '+ str(alp_freq[c]) + ', \n')
fr.write('} \n')

fr.write('Sequence_freq = { \n')
for c in seq_freq:
	fr.write('\'' + str(c) + '\': '+ str(seq_freq[c]) + ', ')
fr.write('} \n')

fr.close()