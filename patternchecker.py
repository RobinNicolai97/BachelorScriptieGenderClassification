#!/usr/bin/env python3


def find_patterns(x):
	file = open(x, 'r') 
	lines = file.readlines()
	filename_gender = x + '_' + 'gender'
	filename_ani = x + '_' + 'animacy'
	outfile_gender = open(filename_gender,'w')
	outfile_ani = open(filename_ani,'w')
	i = 0 #to keep track of progress

	for line in lines:
		line = line.strip().split('\t') 
		print(i)
		gram = [line[0].split(), line[1].split(), line[2]]
		i += 1
		if ('NOUN' in gram[1] and 'PRON' in gram[1]) or ('PROPN' in gram[1] and 'PRON' in gram[1]): 
			string5 = "-".join(gram[1])
			# following patterns are used to detect gender
			#names are indicated as 'NOUN' most of the time, but sometimes they are indicated as 'PROPN'. Therefore, we check for both indications. 
			#pattern with 'zijn':
			if 'PRON-VERB-NOUN' in string5 or 'PRON-VERB-ADV-NOUN' in string5 or 'PRON-VERB-ADV-DET-NOUN' in string5 or 'PRON-VERB-DET-NOUN' in string5 or 'PRON-VERB-PROPN' in string5 or 'PRON-VERB-ADV-PROPN' in string5 or 'PRON-VERB-ADV-DET-PROPN' in string5 or 'PRON-VERB-DET-PROPN' in string5: #checking if certain patterns occur in the 5-gram
				copy_words = gram[0]
				copy_pos = gram[1]
				found = False
				if 'PRON-VERB-DET' in string5:
					while found == False:
						if copy_pos[0] == 'PRON' and copy_pos[1] == 'VERB' and copy_pos[2] == 'DET': #making sure only the pronoun that fits the pattern will be kept and used
							found = True								
						else:
							copy_words = copy_words[1:]	#this is to make sure we know the exact location of the right pronoun
							copy_pos = copy_pos[1:]
				elif 'PRON-VERB-ADV' in string5:
					while found == False:
						if copy_pos[0] == 'PRON' and copy_pos[1] == 'VERB' and copy_pos[2] == 'ADV':
							found = True
						else:
							copy_words = copy_words[1:]	
							copy_pos = copy_pos[1:]
				elif 'PRON-VERB-NOUN' in string5:
					while found == False:
						if copy_pos[0] == 'PRON' and copy_pos[1] == 'VERB' and copy_pos[2] == 'NOUN':
							found = True
						else:
							copy_words = copy_words[1:]
							copy_pos = copy_pos[1:]
				elif 'PRON-VERB-PROPN' in string5:
					while found == False:
						if copy_pos[0] == 'PRON' and copy_pos[1] == 'VERB' and copy_pos[2] == 'PROPN':
							found = True
						else:
							copy_words = copy_words[1:]
							copy_pos = copy_pos[1:]

				if copy_words[copy_pos.index('VERB')] in ['is', 'zijn', 'was', 'waren']:
					indices = [i for i, x in enumerate(copy_pos) if x == "PRON"] #making sure only the pronoun that fits the pattern will be kept and used
					if len(indices) > 1:
						copy_words = copy_words[:indices[1]]
						copy_pos = copy_pos[:indices[1]]

					text =  ' '.join(copy_words)
					pos = ' '.join(copy_pos)
					if copy_words[copy_pos.index('VERB')] in ['is', 'was']: 
						outfile_gender.write(text + '\t' + pos + '\t' + str(gram[2])+ '\t' + 'ZIJN_EV'+'\n') #at the end a mark is added to be able to see which pattern let the 5-gram pass
					elif copy_words[copy_pos.index('VERB')] in ['zijn', 'waren']: 
						outfile_gender.write(text + '\t' + pos + '\t' + str(gram[2])+ '\t' + 'ZIJN_MV'+'\n') 					
						
			#comments above apply to all patterns	

			#pattern with 'en'
			elif 'NOUN-CONJ-PRON' in string5 or 'NOUN-CONJ-ADV-PRON' in string5 or 'PROPN-CONJ-PRON' in string5 or 'PROPN-CONJ-ADV-PRON' in string5:
				copy_words = gram[0]
				copy_pos = gram[1]
				found = False

				if 'NOUN-CONJ-PRON' in string5:
					while found == False:
						if copy_pos[-3] == 'NOUN' and copy_pos[-2] == 'CONJ' and copy_pos[-1] == 'PRON':
							found = True
						else:
							copy_words = copy_words[:-1]
							copy_pos = copy_pos[:-1]

				elif 'CONJ-ADV-PRON' in string5:
					while found == False:
						if copy_pos[-3] == 'CONJ' and copy_pos[-2] == 'ADV' and copy_pos[-1] == 'PRON':
							found = True
						else:
							copy_words = copy_words[:-1]
							copy_pos = copy_pos[:-1]
				elif 'PROPN-CONJ-PRON' in string5:
					while found == False:
						if copy_pos[-3] == 'PROPN' and copy_pos[-2] == 'CONJ' and copy_pos[-1] == 'PRON':
							found = True
						else:
							copy_words = copy_words[:-1]
							copy_pos = copy_pos[:-1]

				indices = [i for i, x in enumerate(copy_pos) if x == "PRON"]
				if len(indices) > 1:
					copy_words = copy_words[indices[-2]+1:]
					copy_pos = copy_pos[indices[-2]+1:]

				indices_conj = [i for i, x in enumerate(copy_pos) if x == "CONJ"] #indication of how many conjunctions are present, to make sure that only 'en' gets through

				if copy_words[indices_conj[-1]] == 'en': #pattern with CONJ only fits if CONJ == 'en'
					text =  ' '.join(copy_words)
					pos = ' '.join(copy_pos)
					outfile_gender.write(text + '\t' + pos + '\t' + str(gram[2])+ '\t' + 'CONJ'+'\n')

			#pattern with 'dat'
			elif 'NOUN-VERB-CONJ-PRON' in string5 or 'NOUN-VERB-ADV-CONJ-PRON' in string5 or 'PROPN-VERB-CONJ-PRON' in string5 or 'PROPN-VERB-ADV-CONJ-PRON' in string5:

				copy_words = gram[0]
				copy_pos = gram[1]
				found = False

				if 'VERB-CONJ-PRON' in string5:
					while found == False:
						if copy_pos[-3] == 'VERB' and copy_pos[-2] == 'CONJ' and copy_pos[-1] == 'PRON':
							found = True
						else:
							copy_words = copy_words[:-1]
							copy_pos = copy_pos[:-1]

				elif 'ADV-CONJ-PRON' in string5:
					while found == False:
						if copy_pos[-3] == 'ADV' and copy_pos[-2] == 'CONJ' and copy_pos[-1] == 'PRON':
							found = True
						else:
							copy_words = copy_words[:-1]
							copy_pos = copy_pos[:-1]



				indices = [i for i, x in enumerate(copy_pos) if x == "PRON"]
				if len(indices) > 1:
					copy_words = copy_words[indices[-2]+1:]
					copy_pos = copy_pos[indices[-2]+1:]

				
				indices_conj = [i for i, x in enumerate(copy_pos) if x == "CONJ"] #indication of how many conjunctions are present, to make sure that only 'dat' gets through

				if copy_words[indices_conj[-1]] == 'dat':#pattern with CONJ only fits if CONJ == 'dat'
					text =  ' '.join(copy_words)
					pos = ' '.join(copy_pos)
					outfile_gender.write(text + '\t' + pos + '\t' + str(gram[2])+ '\t' + 'VERB_DAT'+'\n') 

			#pattern with verb
			elif 'NOUN-VERB-PRON-NOUN' in string5 or 'NOUN-VERB-ADV-PRON-NOUN' in string5 or 'PROPN-VERB-PRON-NOUN' in string5 or 'PROPN-VERB-ADV-PRON-NOUN' in string5 or 'NOUN-VERB-PRON-ADJ-NOUN' in string5 or 'PROPN-VERB-PRON-ADJ-NOUN' in string5 or 'NOUN-VERB-PRON-PROPN' in string5 or 'NOUN-VERB-ADV-PRON-PROPN' in string5 or 'PROPN-VERB-PRON-PROPN' in string5 or 'PROPN-VERB-ADV-PRON-PROPN' in string5 or 'NOUN-VERB-PRON-ADJ-PROPN' in string5 or 'PROPN-VERB-PRON-ADJ-PROPN' in string5:

				copy_words = gram[0]
				copy_pos = gram[1]
				found = False


				if 'VERB-PRON-NOUN' in string5:
					while found == False:
						if copy_pos[-3] == 'VERB' and copy_pos[-2] == 'PRON' and copy_pos[-1] == 'NOUN':
							found = True
						else:
							copy_words = copy_words[:-1]
							copy_pos = copy_pos[:-1]
				if 'VERB-ADV-PRON-NOUN' in string5:
					while found == False:
						if copy_pos[-4] == 'VERB' and copy_pos[-3] == 'ADV' and copy_pos[-2] == 'PRON' and copy_pos[-1] == 'NOUN':
							found = True
						else:
							copy_words = copy_words[:-1]
							copy_pos = copy_pos[:-1]
				if 'VERB-PRON-ADJ-NOUN' in string5:
					while found == False:
						if copy_pos[-4] == 'VERB' and copy_pos[-3] == 'PRON' and copy_pos[-2] == 'ADJ' and copy_pos[-1] == 'NOUN':
							found = True
						else:
							copy_words = copy_words[:-1]
							copy_pos = copy_pos[:-1]
				if 'ADV-PRON-ADJ-NOUN' in string5:
					while found == False:
						if copy_pos[-4] == 'ADV' and copy_pos[-3] == 'PRON' and copy_pos[-2] == 'ADJ' and copy_pos[-1] == 'NOUN':
							found = True
						else:
							copy_words = copy_words[:-1]
							copy_pos = copy_pos[:-1]
				if 'VERB-PRON-PROPN' in string5:
					while found == False:
						if copy_pos[-3] == 'VERB' and copy_pos[-2] == 'PRON' and copy_pos[-1] == 'PROPN':
							found = True
						else:
							copy_words = copy_words[:-1]
							copy_pos = copy_pos[:-1]
				if 'VERB-ADV-PRON-PROPN' in string5:
					while found == False:
						if copy_pos[-4] == 'VERB' and copy_pos[-3] == 'ADV' and copy_pos[-2] == 'PRON' and copy_pos[-1] == 'PROPN':
							found = True
						else:
							copy_words = copy_words[:-1]
							copy_pos = copy_pos[:-1]
				if 'VERB-PRON-ADJ-PROPN' in string5:
					while found == False:
						if copy_pos[-4] == 'VERB' and copy_pos[-3] == 'PRON' and copy_pos[-2] == 'ADJ' and copy_pos[-1] == 'PROPN':
							found = True
						else:
							copy_words = copy_words[:-1]
							copy_pos = copy_pos[:-1]
				if 'ADV-PRON-ADJ-PROPN' in string5:
					while found == False:
						if copy_pos[-4] == 'ADV' and copy_pos[-3] == 'PRON' and copy_pos[-2] == 'ADJ' and copy_pos[-1] == 'PROPN':
							found = True
						else:
							copy_words = copy_words[:-1]
							copy_pos = copy_pos[:-1]



				indices = [i for i, x in enumerate(copy_pos) if x == "PRON"]
				if len(indices) > 1:
					copy_words = copy_words[indices[-2]+1:]
					copy_pos = copy_pos[indices[-2]+1:]

				text =  ' '.join(copy_words)
				pos = ' '.join(copy_pos)
				outfile_gender.write(text + '\t' + pos + '\t' + str(gram[2])+ '\t' + 'VERB_OWN'+'\n')


				
			# following patterns are used to detect animacy
			elif 'NOUN-PUNCT-PRON' in string5 or 'NOUN-PRON' in string5 or 'NOUN-ADP-PRON' in string5 or 'NOUN-PUNCT-ADP-PRON' in string5 or 'PROPN-PUNCT-PRON' in string5 or 'PROPN-PRON' in string5 or 'PROPN-ADP-PRON' in string5 or 'PROPN-PUNCT-ADP-PRON' in string5:
				copy_words = gram[0]
				copy_pos = gram[1]
				found = False

				if 'NOUN-PUNCT-PRON' in string5:
					while found == False:
						if copy_pos[-3] == 'NOUN' and copy_pos[-2] == 'PUNCT' and copy_pos[-1] == 'PRON':
							found = True
						else:
							copy_words = copy_words[:-1]
							copy_pos = copy_pos[:-1]

				elif 'NOUN-PRON' in string5:
					while found == False:
						if copy_pos[-2] == 'NOUN' and copy_pos[-1] == 'PRON':
							found = True
						else:
							copy_words = copy_words[:-1]
							copy_pos = copy_pos[:-1]
				elif 'NOUN-ADP-PRON' in string5:
					while found == False:
						if copy_pos[-3] == 'NOUN' and copy_pos[-2] == 'ADP' and copy_pos[-1] == 'PRON':
							found = True
						else:
							copy_words = copy_words[:-1]
							copy_pos = copy_pos[:-1]

				elif 'PUNCT-ADP-PRON' in string5:
					while found == False:
						if copy_pos[-3] == 'PUNCT' and copy_pos[-2] == 'ADP' and copy_pos[-1] == 'PRON':
							found = True
						else:
							copy_words = copy_words[:-1]
							copy_pos = copy_pos[:-1]

				elif 'PROPN-PUNCT-PRON' in string5:
					while found == False:
						if copy_pos[-3] == 'PROPN' and copy_pos[-2] == 'PUNCT' and copy_pos[-1] == 'PRON':
							found = True
						else:
							copy_words = copy_words[:-1]
							copy_pos = copy_pos[:-1]

				elif 'PROPN-PRON' in string5:
					while found == False:
						if copy_pos[-2] == 'PROPN' and copy_pos[-1] == 'PRON':
							found = True
						else:
							copy_words = copy_words[:-1]
							copy_pos = copy_pos[:-1]
				elif 'PROPN-ADP-PRON' in string5:
					while found == False:
						if copy_pos[-3] == 'PROPN' and copy_pos[-2] == 'ADP' and copy_pos[-1] == 'PRON':
							found = True
						else:
							copy_words = copy_words[:-1]
							copy_pos = copy_pos[:-1]

				indices = [i for i, x in enumerate(copy_pos) if x == "PRON"]
				if len(indices) > 1:
					copy_words = copy_words[indices[-2]+1:]
					copy_pos = copy_pos[indices[-2]+1:]

				
				indices_punct = [i for i, x in enumerate(copy_pos) if x == "PUNCT"] #indication of how many punctuation is present, to make sure that only commas get through

				if ('PUNCT' in copy_pos and copy_words[indices_punct[-1]] == ',') or 'PUNCT' not in copy_pos: #pattern with PUNCT only fits if PUNCT == a comma
					pattern_type = 'BLANK' # checking what type of pattern found the match
					if 'PUNCT' in copy_pos and 'ADP' in copy_pos:
						pattern_type = 'PUNCT-ADP'
					elif 'PUNCT' in copy_pos:
						pattern_type = 'PUNCT'
					elif 'ADP' in copy_pos:
						pattern_type = 'ADP'
					text =  ' '.join(copy_words)
					pos = ' '.join(copy_pos)
					outfile_ani.write(text + '\t' + pos + '\t' + str(gram[2])+'\t'+ pattern_type+'\n')


                 
def main():
	for i in range(0, 12):
		file = '5gm-00'+str(i)+'-annotated'
		find_patterns(file)
	print('Done!') 
if __name__ == '__main__':
	main()

