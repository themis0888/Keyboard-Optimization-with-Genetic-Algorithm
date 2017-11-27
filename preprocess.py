from collections import Counter


'''
preprocess : string(file name) -> dict(for char), dict(for seq)
dict : set of {(string) : float}
Example : preprocess()
Eat the name of textfile(as a string) and calculate the frequency
of each aphabet and every sequence. 
'''

def preprocess(filename = 'text.txt'):

	f = open('text.txt', 'r')
	chr_list = []
	lines = f.read()
	line_lst = list(lines.lower())
	for c in line_lst:
		if c.isalpha() or c:
			chr_list.append(c)
	rel_list = []
	for i in range(len(chr_list)-1):
		rel_list.append(chr_list[i]+chr_list[i+1])
	alp_freq = Counter(chr_list)
	seq_freq = Counter(rel_list)

	for i in alp_freq:
		alp_freq[i] /= len(chr_list)
	for i in seq_freq:
		seq_freq[i] /= len(rel_list)

	return alp_freq, seq_freq




