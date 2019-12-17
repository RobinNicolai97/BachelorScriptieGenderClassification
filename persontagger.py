#!/usr/bin/env python3
import pickle
import nltk
from nltk import word_tokenize
from nltk.util import ngrams
import string
import re



def find_gender(): 
	genderdict = {} # NOUN : number male, number female, number neutral, number plural	
	pickle_out = open("dict_gender.pickle","wb")
	for i in range(0,12):
		filename_gender = '5gm-00'+str(i)+ '-annotated_gender'
		file = open(filename_gender, 'r') 
		for line in file.readlines():
			position = None #used later to check position of NOUNS, to check if they are consecutive. 
			noun = ''
			split = line.split('\t')
			pattern = [split[0].split(), split[1].split(), int(split[2]), split[3].strip()]
			nouns = split[1].split() #duplicate of pattern[1] to delete out of containing all part of speech
			words = split[0].split() #duplicate of pattern[0] to delete out of containing all words
			for pos in pattern[1]:
				if pos == 'NOUN' or pos == 'PROPN' :
					if words[nouns.index(pos)].isalpha(): # a lot of symbols are  also tagged as NOUN
						if position == nouns.index(pos):
							position1 = nouns.index(pos)
							noun += words[nouns.index(pos)] + ' '
							del words[nouns.index(pos)] #if after deleting this NOUN, another NOUN is in this place, we know they are consecutive 
							del nouns[nouns.index(pos)] #...consecutive NOUNS will be assumed to belong together
						else: 
							if position == None:							
								position = nouns.index(pos)
								noun = words[nouns.index(pos)] + ' '
								del words[nouns.index(pos)]
								del nouns[nouns.index(pos)]
							else:	#there can be multiple independent sequences of NOUNS. 
								if pattern[3] != 'ZIJN': #for this pattern, we need the first sequence of NOUNS, for the others we need te last. 
									position = nouns.index(pos) #..this is because of the forms of the different patterns
									noun = words[nouns.index(pos)] + ' '
									del words[nouns.index(pos)]
									del nouns[nouns.index(pos)]
									
					else:
						del words[nouns.index(pos)]
						del nouns[nouns.index(pos)]
						if position != None:
							position = position -1 #starting new sequence of NOUNS after a non-alphabetic symbol
						
			noun_all = noun.strip()
			del noun
			if len(noun_all.split()) > 1: #For example, in 'Queen Beatrix', we want information about 'Queen Beatrix' being female, as well as information about 'Queen' being female and 'Beatrix' being female. 
				noun_all = [noun_all] + noun_all.split()
			else:
				noun_all = [noun_all]

			if len(noun_all) > 3: #assuming 3 names is the maximum length of a person in the next two lines
				noun_all.append( ' '.join(noun_all[1:3])) 			
				noun_all.append( ' '.join(noun_all[2:4]))

			for noun in noun_all:
				
				if noun != '':	
	
					if (pattern[0][pattern[1].index('PRON')] == 'hij' and pattern[3] in ['ZIJN', 'VERB_DAT']) or (pattern[0][pattern[1].index('PRON')] == 'zijn' and pattern[3] in ['CONJ', 'VERB_DAT', 'VERB_OWN']) : #pronouns are being used for gender information. different patterns allow different sorts of words. pattern[3] is the type of pattern that found the NOUN and PRON.
						if noun in genderdict.keys():            		
							genderdict[noun][0] += pattern[2] #if a NOUN is already in the knowledge base, we update information about it
						else:
							genderdict.update({noun: [pattern[2], 0,0,0]})  # if a NOUN is new to the knowledge base, we add it
					elif (pattern[0][pattern[1].index('PRON')] in ['zij', 'ze'] and pattern[3] in ['ZIJN', 'VERB_DAT']) or (pattern[0][pattern[1].index('PRON')] == 'haar'  and pattern[3] in ['CONJ', 'VERB_DAT', 'VERB_OWN']) :
						if noun in genderdict.keys():            		
							genderdict[noun][1] += pattern[2]
						else:
							genderdict.update({noun: [0,pattern[2],0,0]})  
					elif pattern[0][pattern[1].index('PRON')] == 'het' and pattern[3] in ['ZIJN', 'VERB_DAT']:
						if noun in genderdict.keys():            		
							genderdict[noun][2] += pattern[2]
						else:
							genderdict.update({noun: [0,0,pattern[2],0]})  
					elif (pattern[0][pattern[1].index('PRON')] == 'henzelf' and pattern[3] == 'VERB_OWN') or (pattern[0][pattern[1].index('PRON')] == 'hun'  and pattern[3] in ['CONJ', 'VERB_DAT', 'VERB_OWN']) or (pattern[0][pattern[1].index('PRON')] == 'elkaar' and pattern[3] == 'VERB_OWN'):
						if noun in genderdict.keys():            		
							genderdict[noun][3] += pattern[2]
						else:
							genderdict.update({noun: [0,0,0,pattern[2]]})
					elif pattern[0][pattern[1].index('PRON')] == 'zichzelf' and pattern[3] == 'VERB_OWN': #zichzelf provides information about 'not plural'. The pattern counts for all non-plural classes in this case. 
						if noun in genderdict.keys():            		
							genderdict[noun][0] += pattern[2]
							genderdict[noun][1] += pattern[2]
							genderdict[noun][2] += pattern[2]
						else:
							genderdict.update({noun: [pattern[2], pattern[2],pattern[2],0]})    
	pickle.dump(genderdict, pickle_out)

	

def find_animacy(): #most comments for this function are equal to those of find_gender(), they can therefore be found over there. 
	animacydict = {} # NOUN: number animate, number inanimate.
	pickle_out = open("dict_animacy.pickle","wb")
	for i in range(0,12):
		filename_ani = '5gm-00'+str(i)+ '-annotated_animacy'
		file = open(filename_ani, 'r') 
		for line in file.readlines():
			position = None
			noun = ''
			split = line.split('\t')
			pattern = [split[0].split(), split[1].split(), int(split[2])]
			nouns = split[1].split() 
			words = split[0].split() 
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
							del words[nouns.index(pos)]
							del nouns[nouns.index(pos)]
							if position != None:
								position = position -1 
			noun_all = noun.strip()
			del noun
			if len(noun_all.split()) > 1:
				noun_all = [noun_all] + noun_all.split()
			else:
				noun_all = [noun_all]

			if len(noun_all) > 3: 
				noun_all.append( ' '.join(noun_all[1:3])) 			
				noun_all.append( ' '.join(noun_all[2:4])) 
			for noun in noun_all:
				if noun != '': 
					if 'PRON' in pattern[1]:
						if pattern[0][pattern[1].index('PRON')] == 'wie': #since there's only one pattern for animacy, we don't need to check patterns here
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
			gender = options[freqs.index(max(freqs))] #the most common gender will be assumed right
			freq = max(freqs)
			del freqs[freqs.index(max(freqs))]
			if max(freqs) == 0:#as a certainty measure, we calculate distances between the highest and second highest frequencies of genders. 
				confidence = freq
			else: 			
				confidence = freq/max(freqs)
			dic.update({key: (gender, confidence)}) 
	return dic

				
def most_frequent_animacy():
	dic = pickle.load( open( "dict_animacy.pickle", "rb" ) )
	options = ['animate', 'inanimate']
	for key in dic.keys():
		freqs = dic[key]
		if freqs.count(max(freqs)) > 1:
			dic.update({key: ('not sure, equal freqs', max(freqs))}) 
		else:
			animacy = options[freqs.index(max(freqs))]
			freq = max(freqs)
			del freqs[freqs.index(max(freqs))]
			if max(freqs) == 0:
				confidence = freq
			else:
				confidence = freq/max(freqs)
			dic.update({key: (animacy, confidence)}) 
	return dic
	
def most_frequent_combined(dic_gender, dic_animacy):
	dic_combined = {}
	for key in dic_gender.keys(): # all keys in dic_gender are assumed to be a more specific classification of animate
		if key in dic_animacy.keys():
			if dic_animacy[key][1] > dic_gender[key][1] and dic_animacy[key][0] == 'inanimate': # if inanimate is more frequent than the most frequent gender, inanimate gets priority.
				dic_combined.update({key: ('inanimate', dic_animacy[key][1])})
				
			else:
				dic_combined.update({key: (dic_gender[key][0], dic_gender[key][1])}) #if the most frequent gender is more frequent than inanimate, the gender gets priority
			del dic_animacy[key]
		else:
			dic_combined.update({key: (dic_gender[key][0], dic_gender[key][1])})
	for key in dic_animacy.keys(): #all non-overlapping knowledge between both will be put together instantly. 
		dic_combined.update({key:(dic_animacy[key][0], dic_animacy[key][1])}) 

	return dic_combined


def create_candidates(): #extracting words without annotation, to be annotated by the machine
	for i in range(1, 5):
		file = open('Test/'+ str(i)+'_annotated' , 'r') 
		outfile = open('Test/'+ str(i)+'_words','w')
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
			bigrams = zip(*[line.split()[i:] for i in range(2)])
			bigrams = [" ".join(ngram) for ngram in bigrams]
			trigrams = zip(*[line.split()[i:] for i in range(3)])
			trigrams = [" ".join(ngram) for ngram in trigrams]
			if option1.lower() in combined_dict.keys(): #first priority: the whole sequence of words (can also be a single word)
				outfile.write(option1 + '\t' + combined_dict[option1.lower()][0] + '\n')

			else: 
				gender = 'Not in Knowledge Base'
				freq = 0 #this is the certainty measure calculated in the 'most_frequent_' functions. 
				for trigram in trigrams: #second priority: trying to match a trigram
					trigram = trigram.lower()
					if trigram in combined_dict.keys():
						if combined_dict[trigram][1] > freq: # if a match beats the certainty score of the previous match, it gets priority
							gender = combined_dict[trigram][0]
							freq = combined_dict[trigram][1]

				if freq == 0:
					for bigram in bigrams:  #third priority: trying to match a bigram
						bigram = bigram.lower()
						if bigram in combined_dict.keys():
							if combined_dict[bigram][1] > freq:
								gender = combined_dict[bigram][0]
								freq = combined_dict[bigram][1]
					if freq == 0: 
						line = line.split() 
						for unigram in line: #if nothing has been found, try to match single words. 
							word = unigram.lower()
							if word in combined_dict.keys():
								if combined_dict[word][1] > freq:
									gender = combined_dict[word][0]
									freq = combined_dict[word][1]
				outfile.write(' '.join(line) + '\t' + gender + '\n')
def accuracy_test():
	classifications_human = []
	classifications_machine = []
	wrong_pairs = [] # it's interesting to see what kinds of misclassifications occur most often
	for i in range(1,24):
		human = open('Test/'+str(i)+'_annotated','r')
		machine = open('Test/'+str(i)+'_machine_annotation','r')
		for line in human.readlines():
			if len(line.split('\t')) >1:
				classifications_human.append(line.split('\t')[1].strip())

		for line in machine.readlines():
			if len(line.split('\t')) >1:
				classifications_machine.append(line.split('\t')[1].strip())
	#numbers for keeping track of correct classification:
	correct_male = 0
	correct_female = 0
	correct_neutral = 0
	correct_plural = 0
	correct_inanimate = 0
	#other interesting counts:
	not_in_KB = 0 #we want to see how often the machine has no information available for the candidate
	animate = 0 #since animate is a less specific classification instead of a wrong one, we keep track of it
	
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
	print('Male: ', (correct_male/381) *100,'%', '\n', 'Female: ', (correct_female/33)*100,'%', '\n', 'Neutral: ', (correct_neutral/170)*100,'%', '\n', 'Plural: ', (correct_plural/838)*100,'%', '\n', 'Inanimate: ', (correct_inanimate/2728)*100,'%', '\n', 'Not in KB: ', (not_in_KB/4150)*100,'%', '\n', 'No Gender Known, but Animate: ', animate, '\n\n')
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

