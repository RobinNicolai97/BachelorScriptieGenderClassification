#!/usr/bin/env python3
import pickle
import nltk
from nltk import word_tokenize
from nltk.util import ngrams
import string




def find_gender(): 
	genderdict = {} # NOUN : number male, number female, number neutral, number plural	
	pickle_out = open("dict_gender.pickle","wb")
	for i in range(0,12):
		filename_gender = '5gm-00'+str(i)+ '-annotated_gender'
		file = open(filename_gender, 'r') 
		for line in file.readlines():
			position = None
			noun = ''
			split = line.split('\t')
			pattern = [split[0].split(), split[1].split(), int(split[2])]
			nouns = split[1].split() #duplicate of pattern[1] to delete out of
			words = split[0].split() #duplicate of pattern[0] to delete out of
			for pos in pattern[1]:
				if pos == 'NOUN' or pos == 'PROPN' :
					if words[nouns.index(pos)].isalpha():
						if position == nouns.index(pos):
							position1 = nouns.index(pos)
							noun += words[nouns.index(pos)] + ' '
							del words[nouns.index(pos)]
							del nouns[nouns.index(pos)]
						else: 
							position = nouns.index(pos)
							noun = words[nouns.index(pos)] + ' '
							del words[nouns.index(pos)]
							del nouns[nouns.index(pos)]
			noun_all = noun.strip()
			del noun
			noun_all = [noun_all] + noun_all.split()
			if len(noun_all) > 3: #assuming 3 names is maximum length of a person
				noun_all + noun_all[1:3] + noun_all[2:4] 
				
			
			
			for noun in noun_all:
				
				if noun != '':	
	
					if pattern[0][pattern[1].index('PRON')] == 'hij' or pattern[0][pattern[1].index('PRON')] == 'zijn':
						if noun in genderdict.keys():            		
							genderdict[noun][0] += pattern[2]
						else:
							genderdict.update({noun: [pattern[2], 0,0,0]})  
					elif pattern[0][pattern[1].index('PRON')] == 'zij' or pattern[0][pattern[1].index('PRON')] == 'ze' or pattern[0][pattern[1].index('PRON')] == 'haar':
						if noun in genderdict.keys():            		
							genderdict[noun][1] += pattern[2]
						else:
							genderdict.update({noun: [0,pattern[2],0,0]})  
					elif pattern[0][pattern[1].index('PRON')] == 'het':
						if noun in genderdict.keys():            		
							genderdict[noun][2] += pattern[2]
						else:
							genderdict.update({noun: [0,0,pattern[2],0]})  
					elif pattern[0][pattern[1].index('PRON')] == 'hen' or pattern[0][pattern[1].index('PRON')] == 'henzelf' or pattern[0][pattern[1].index('PRON')] == 'hun' or pattern[0][pattern[1].index('PRON')] == 'elkaar':
						if noun in genderdict.keys():            		
							genderdict[noun][3] += pattern[2]
						else:
							genderdict.update({noun: [0,0,0,pattern[2]]})
					#elif pattern[0][pattern[1].index('PRON')] == 'zichzelf':
					#	if noun in genderdict.keys():            		
					#		genderdict[noun][0] += pattern[2]
					#		genderdict[noun][1] += pattern[2]
					#		genderdict[noun][2] += pattern[2]
					#	else:
					#		genderdict.update({noun: [pattern[2], pattern[2],pattern[2],0]})    
	pickle.dump(genderdict, pickle_out)

	

def find_animacy(): 
	animacydict = {} # NOUN/ADJ : number animate, number inanimate.
	pickle_out = open("dict_animacy.pickle","wb")
	for i in range(0,12):
		filename_ani = '5gm-00'+str(i)+ '-annotated_animacy'
		file = open(filename_ani, 'r') 
		for line in file.readlines():
			position = None
			noun = ''
			split = line.split('\t')
			pattern = [split[0].split(), split[1].split(), int(split[2])]
			nouns = split[1].split() #duplicate of pattern[1] to delete out of
			words = split[0].split() #duplicate of pattern[0] to delete out of
			if 'NOUN' in pattern[1] or 'PROPN' in pattern[1]:
				for pos in pattern[1]:
					if pos == 'NOUN' or pos == 'PROPN':
						if words[nouns.index(pos)].isalpha():
							if position == nouns.index(pos):
								position1 = nouns.index(pos)
								noun += words[nouns.index(pos)] + ' '
								del words[nouns.index(pos)]
								del nouns[nouns.index(pos)]
							else: 
								position = nouns.index(pos)
								noun = words[nouns.index(pos)] + ' '
								del words[nouns.index(pos)]
								del nouns[nouns.index(pos)]
			else:
				for pos in pattern[1]:
					if pos == 'ADJ':
						if words[nouns.index(pos)].isalpha():
							if position == nouns.index(pos):
								position1 = nouns.index(pos)
								noun += words[nouns.index(pos)] + ' '
								del words[nouns.index(pos)]
								del nouns[nouns.index(pos)]
							else: 
								position = nouns.index(pos)
								noun = words[nouns.index(pos)] + ' '
								del words[nouns.index(pos)]
								del nouns[nouns.index(pos)]
			noun_all = noun.strip()
			del noun
			noun_all = [noun_all] + noun_all.split()
			if len(noun_all) > 3: #assuming 3 names is maximum length of a person
				noun_all + noun_all[1:3] + noun_all[2:4] 
			for noun in noun_all:
				if noun != '': 
					if 'PRON' in pattern[1]:
						if pattern[0][pattern[1].index('PRON')] == 'wie':
							if noun in animacydict.keys():            		
								animacydict[noun][0] += pattern[2]
							else:
								animacydict.update({noun: [pattern[2], 0]}) 
						elif pattern[0][pattern[1].index('PRON')] == 'welke' or pattern[0][pattern[1].index('PRON')] == 'wat':
							if noun in animacydict.keys():            		
								animacydict[noun][1] += pattern[2]
							else:
								animacydict.update({noun: [0,pattern[2]]}) 
	pickle.dump(animacydict, pickle_out)

def most_frequent_gender():
	dic = pickle.load( open( "dict_gender.pickle", "rb" ) )
	options = ['male', 'female', 'neutral', 'plural']
	for key in dic.keys():
		freqs = dic[key]
		if freqs.count(max(freqs)) > 1:
			dic.update({key: ('not sure, equal freqs', max(freqs))}) 
		else:
			dic.update({key: (options[freqs.index(max(freqs))], max(freqs))}) 
	return dic

				
def most_frequent_animacy():
	dic = pickle.load( open( "dict_animacy.pickle", "rb" ) )
	options = ['animate', 'inanimate']
	for key in dic.keys():
		freqs = dic[key]
		if freqs.count(max(freqs)) > 1:
			dic.update({key: ('not sure, equal freqs', max(freqs))}) 
		else:
			dic.update({key: (options[freqs.index(max(freqs))], max(freqs))}) 
	return dic
	
def most_frequent_combined(dic_gender, dic_animacy):
	dic_combined = {}
	for key in dic_gender.keys():
		if key in dic_animacy.keys():
			if dic_animacy[key][1] > dic_gender[key][1] and dic_animacy[key][0] == 'inanimate':
				dic_combined.update({key: ('inanimate', dic_animacy[key][1])})
				
			else:
				#print(dic_gender[key][0]) 
				dic_combined.update({key: (dic_gender[key][0], dic_gender[key][1])})
			del dic_animacy[key]
		else:
			#print(dic_gender[key][0]) 
			dic_combined.update({key: (dic_gender[key][0], dic_gender[key][1])})
	for key in dic_animacy.keys():
		dic_combined.update({key:(dic_animacy[key][0], dic_animacy[key][1])}) 

	return dic_combined


def create_candidates():
	for i in range(1, 5):
		file = open('Development/'+ str(i)+'_annotated' , 'r') 
		outfile = open('Development/'+ str(i)+'_words','w')
		lines = file.readlines()
		for line in lines:
			if len(line.split()) > 0:
				outfile.write(line.split('\t')[0] + '\n')
				
				
				


def check_KB(combined_dict):

	for i in range(1,24):
		outfile = open('Test/'+str(i)+'_machine_annotation','w')
		file =  open('Test/'+str(i)+'_words','r')

		for line in file.readlines():
			line = line.strip()
			option1 = line
			if option1.lower() in combined_dict.keys():
				outfile.write(option1 + '\t' + combined_dict[option1.lower()][0] + '\n')
			else: 
				line = line.split()
				gender = 'Not in Knowledge Base'
				freq = 0
				for word in line:
					word = word.lower()
					if word in combined_dict.keys():
						if combined_dict[word][1] > freq:
							gender = combined_dict[word][0]
							freq = combined_dict[word][1]
				outfile.write(' '.join(line) + '\t' + gender + '\n')
def accuracy_test():
	classifications_human = []
	classifications_machine = []
	wrong_pairs = []
	for i in range(1,24):
		human = open('Test/'+str(i)+'_annotated','r')
		machine = open('Test/'+str(i)+'_machine_annotation','r')
		for line in human.readlines():
			if len(line.split('\t')) >1:
				classifications_human.append(line.split('\t')[1].strip())

		for line in machine.readlines():
			if len(line.split('\t')) >1:
				classifications_machine.append(line.split('\t')[1].strip())

	correct_male = 0
	correct_female = 0
	correct_neutral = 0
	correct_plural = 0
	correct_inanimate = 0
	not_in_KB = 0
	animate = 0
	
	for i in range(0, len(classifications_human)):
		if classifications_human[i] == 'male':
			if classifications_machine[i] == 'male':
				correct_male += 1
			else:
				if classifications_machine[i] == 'Not in Knowledge Base':
					not_in_KB += 1
				elif classifications_machine[i] == 'animate':
					animate += 1
				wrong_pairs.append(('male', classifications_machine[i]))

		if classifications_human[i] == 'female':
			if classifications_machine[i] == 'female':
				correct_female += 1
			else:
				if classifications_machine[i] == 'Not in Knowledge Base':
					not_in_KB += 1
				elif classifications_machine[i] == 'animate':
					animate += 1
				wrong_pairs.append(('female', classifications_machine[i]))

		if classifications_human[i] == 'neutral':
			if classifications_machine[i] == 'neutral':
				correct_neutral += 1
			else:
				if classifications_machine[i] == 'Not in Knowledge Base':
					not_in_KB += 1
				elif classifications_machine[i] == 'animate':
					animate += 1
				wrong_pairs.append(('neutral', classifications_machine[i]))

		if classifications_human[i] == 'plural':
			if classifications_machine[i] == 'plural':
				correct_plural += 1
			else:
				if classifications_machine[i] == 'Not in Knowledge Base':
					not_in_KB += 1
				elif classifications_machine[i] == 'animate':
					animate += 1
				wrong_pairs.append(('plural', classifications_machine[i]))

		if classifications_human[i] == 'inanimate':
			if classifications_machine[i] == 'inanimate':
				correct_inanimate += 1
			else:
				if classifications_machine[i] == 'Not in Knowledge Base':
					not_in_KB += 1
				wrong_pairs.append(('inanimate', classifications_machine[i]))
	print('Accuracy scores per class: \n')
	print('Male: ', (correct_male/381) *100,'%', '\n', 'Female: ', (correct_female/33)*100,'%', '\n', 'Neutral: ', (correct_neutral/170)*100,'%', '\n', 'Plural: ', (correct_plural/838)*100,'%', '\n', 'Inanimate: ', (correct_inanimate/2728)*100,'%', '\n', 'Not in KB: ', (not_in_KB/4150)*100,'%', '\n', 'No Gender: ', animate, '\n\n')
	print('What went wrong?    (human annotation - machine annotation)')
	for pair in set(wrong_pairs):
		print(pair[0], ' - ', pair[1], ' : ', wrong_pairs.count(pair))








			


                 
def main():
	find_gender()
	freq_dic_gender = most_frequent_gender()
	find_animacy()
	freq_dic_animacy = most_frequent_animacy()
	combined_dict = most_frequent_combined(freq_dic_gender, freq_dic_animacy)
	candidates = create_candidates()
	check_KB(combined_dict)
	accuracy_test()

if __name__ == '__main__':
	main()

