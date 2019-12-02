#!/usr/bin/env python3


def find_patterns(x):
	file = open(x, 'r') 
	lines = file.readlines()
	filename_gender = x + '_' + 'gender'
	filename_ani = x + '_' + 'animacy'
	outfile_gender = open(filename_gender,'w')
	outfile_ani = open(filename_ani,'w')
	i = 0

	for line in lines:
		line = line.split('\t') 
		print(i)
		gram = [line[0].split(), line[1].split(), line[2].strip()]
		i += 1
		if 'NOUN' in gram[1] and 'PRON' in gram[1] or 'PROPN' in gram[1] and 'PRON' in gram[1]: 
			string5 = "-".join(gram[1])
			#gender
			if 'VERB' in gram[1] and (gram[0][gram[1].index('VERB')] == 'is' or gram[0][gram[1].index('VERB')] == 'zijn' or gram[0][gram[1].index('VERB')] =='was' or gram[0][gram[1].index('VERB')] == 'waren'): 
				if 'NOUN' in gram[1]:
					if gram[1].index('NOUN') < gram[1].index('PRON') and gram[1].index('PRON') > gram[1].index('VERB') and gram[1].index('VERB') > gram[1].index('NOUN'):
						text =  ' '.join(gram[0][gram[1].index('NOUN'):gram[1].index('PRON')+1])
						pos = ' '.join(gram[1][gram[1].index('NOUN'):gram[1].index('PRON')+1])
						outfile_gender.write(text + '\t' + pos + '\t' + str(gram[2])+ '\t' + 'NOM+ADJ'+'\n')
					elif gram[1].index('PRON') < gram[1].index('NOUN') and gram[1].index('NOUN') > gram[1].index('VERB') and gram[1].index('VERB') >  gram[1].index('PRON'):
						text =  ' '.join(gram[0][gram[1].index('PRON'):])
						pos = ' '.join(gram[1][gram[1].index('PRON'):])
						outfile_gender.write(text + '\t' + pos + '\t' + str(gram[2])+ '\t' + 'NOM+ADJ'+'\n')
				elif 'PROPN' in gram[1]:
					if gram[1].index('PROPN') < gram[1].index('PRON') and gram[1].index('PRON') > gram[1].index('VERB') and gram[1].index('VERB') > gram[1].index('PROPN'):
						text =  ' '.join(gram[0][gram[1].index('PROPN'):gram[1].index('PRON')+1])
						pos = ' '.join(gram[1][gram[1].index('PROPN'):gram[1].index('PRON')+1])
						outfile_gender.write(text + '\t' + pos + '\t' + str(gram[2])+ '\t' + 'NOM+ADJ'+'\n')
					elif gram[1].index('PRON') < gram[1].index('PROPN') and gram[1].index('PROPN') > gram[1].index('VERB') and gram[1].index('VERB') >  gram[1].index('PRON'):
						text =  ' '.join(gram[0][gram[1].index('PRON'):])
						pos = ' '.join(gram[1][gram[1].index('PRON'):])
						outfile_gender.write(text + '\t' + pos + '\t' + str(gram[2])+ '\t' + 'NOM+ADJ'+'\n')
						

			elif 'NOUN-CONJ-PRON' in string5 or 'NOUN-CONJ-ADV-PRON' in string5:
				text =  ' '.join(gram[0][gram[1].index('NOUN'):gram[1].index('PRON')+1])
				pos = ' '.join(gram[1][gram[1].index('NOUN'):gram[1].index('PRON')+1])
				outfile_gender.write(text + '\t' + pos + '\t' + str(gram[2])+ '\t' + 'CONJ'+'\n')

			elif 'PROPN-CONJ-PRON' in string5 or 'PROPN-CONJ-ADV-PRON' in string5:
				if 'NOUN' in gram[1] and gram[1].index('NOUN') < gram[1].index('PROPN'): 
					text =  ' '.join(gram[0][gram[1].index('NOUN'):gram[1].index('PRON')+1])
					pos = ' '.join(gram[1][gram[1].index('NOUN'):gram[1].index('PRON')+1])
					outfile_gender.write(text + '\t' + pos + '\t' + str(gram[2])+ '\t' + 'CONJ'+'\n')
				else:
					text =  ' '.join(gram[0][gram[1].index('PROPN'):gram[1].index('PRON')+1])
					pos = ' '.join(gram[1][gram[1].index('PROPN'):gram[1].index('PRON')+1])
					outfile_gender.write(text + '\t' + pos + '\t' + str(gram[2])+ '\t' + 'CONJ'+'\n')

			#elif 'NOUN-VERB-CONJ-PRON' in string5 or 'NOUN-VERB-ADV-CONJ-PRON' in string5:
			#	text =  ' '.join(gram[0][gram[1].index('NOUN'):gram[1].index('PRON')+1])
			#	pos = ' '.join(gram[1][gram[1].index('NOUN'):gram[1].index('PRON')+1])
			#	outfile_gender.write(text + '\t' + pos + '\t' + str(gram[2])+ '\t' + 'VERB+NOM'+'\n')

			#elif 'NOUN-VERB-PRON' in string5 or 'NOUN-VERB-ADV-PRON' in string5:
			#	text =  ' '.join(gram[0][gram[1].index('NOUN'):gram[1].index('PRON')+1])
			#	pos = ' '.join(gram[1][gram[1].index('NOUN'):gram[1].index('PRON')+1])
			#	outfile_gender.write(text + '\t' + pos + '\t' + str(gram[2])+ '\t' + 'VERB+OWN'+'\n')
				
			#animacy
			elif 'NOUN-PUNCT-PRON' in string5 or 'NOUN-PRON' in string5 or 'NOUN-ADP-PRON' in string5 or 'NOUN-PUNCT-ADP-PRON' in string5:
				#index_noun = gram[1].index('NOUN')
				#if 'ADP' not in gram[0:index_noun] and 'NOUN' not in gram[0:index_noun] and 'ADJ' not in gram[0:index_noun]:
				text =  ' '.join(gram[0][gram[1].index('NOUN'):gram[1].index('PRON')+1])
				pos = ' '.join(gram[1][gram[1].index('NOUN'):gram[1].index('PRON')+1])
				outfile_ani.write(text + '\t' + pos + '\t' + str(gram[2])+'\n')
			elif 'PROPN-PUNCT-PRON' in string5 or 'PROPN-PRON' in string5 or 'PROPN-ADP-PRON' in string5 or 'PROPN-PUNCT-ADP-PRON' in string5:
				#index_noun = gram[1].index('NOUN')
				#if 'ADP' not in gram[0:index_noun] and 'NOUN' not in gram[0:index_noun] and 'ADJ' not in gram[0:index_noun]:
				if 'NOUN' in gram[1] and gram[1].index('NOUN') < gram[1].index('PROPN'):
					text =  ' '.join(gram[0][gram[1].index('NOUN'):gram[1].index('PRON')+1])
					pos = ' '.join(gram[1][gram[1].index('NOUN'):gram[1].index('PRON')+1])
					outfile_ani.write(text + '\t' + pos + '\t' + str(gram[2])+'\n')
				else:
					text =  ' '.join(gram[0][gram[1].index('PROPN'):gram[1].index('PRON')+1])
					pos = ' '.join(gram[1][gram[1].index('PROPN'):gram[1].index('PRON')+1])
					outfile_ani.write(text + '\t' + pos + '\t' + str(gram[2])+'\n')
			#elif 'ADJ-PUNCT-PRON' in string5 or 'ADJ-PRON' in string5 or 'ADJ-ADP-PRON' in string5 or 'ADJ-PUNCT-ADP-PRON' in string5:
			#	index_adj = gram[1].index('ADJ')
			#	if 'ADP' not in gram[0:index_adj] and 'NOUN' not in gram[0:index_adj] and 'ADJ' not in gram[0:index_adj]:
			#		text =  ' '.join(gram[0][gram[1].index('ADJ'):gram[1].index('PRON')+1])
			#		pos = ' '.join(gram[1][gram[1].index('ADJ'):gram[1].index('PRON')+1])
			#		outfile_ani.write(text + '\t' + pos + '\t' + str(gram[2])+'\n')

			#elif 'NOUN-ADV' in string5 or 'NOUN-PUNCT-ADV' in string5:
			#	index_noun = gram[1].index('NOUN')
			#	if 'ADP' not in gram[0:index_noun] and 'NOUN' not in gram[0:index_noun] and 'ADJ' not in gram[0:index_noun]:
			#		text =  ' '.join(gram[0][gram[1].index('NOUN'):gram[1].index('ADV')+1])
			#		pos = ' '.join(gram[1][gram[1].index('NOUN'):gram[1].index('ADV')+1])
			#		outfile_ani.write(text + '\t' + pos + '\t' + str(gram[2])+'\n')

			#elif 'ADJ-ADV' in string5 or 'ADJ-PUNCT-ADV' in string5:
			#	index_adj = gram[1].index('ADJ')
			#	if 'ADP' not in gram[0:index_adj] and 'NOUN' not in gram[0:index_adj] and 'ADJ' not in gram[0:index_adj]:
			#		text =  ' '.join(gram[0][gram[1].index('ADJ'):gram[1].index('ADV')+1])
			#		pos = ' '.join(gram[1][gram[1].index('ADJ'):gram[1].index('ADV')+1])
			#		outfile_ani.write(text + '\t' + pos + '\t' + str(gram[2])+'\n')

                 
def main():
	for i in range(0, 12):
		file = '5gm-00'+str(i)+'-annotated'
		find_patterns(file)
	print('Done!') 
if __name__ == '__main__':
	main()

