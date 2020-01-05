#!/usr/bin/env python3
import pickle
import nltk
from nltk import word_tokenize
from nltk.util import ngrams
import string
import re



def find_gender(): 
	#KB's
	#male
	hij_zijn = {}
	hij_dat = {}
	zijn_conj = {}
	zijn_dat = {}
	zijn_ww = {}
	#female
	zij_zijn = {}
	haar_conj = {}
	haar_dat = {}
	haar_ww = {}
	#neutral
	het_zijn = {}
	het_dat = {}
	#plural
	plural_zijn = {}
	hun_conj = {}
	hun_dat = {}
	hun_ww = {}
	elkaars_ww = {}


	pickle_out = open("dict_gender.pickle","wb")
	for i in range(0,12):
		filename_gender = '5gm-00'+str(i)+ '-annotated_gender'
		file = open(filename_gender, 'r') 
		for line in file.readlines():
			position = None #used later to check position of NOUNS, to check if they are consecutive. 
			noun = ''
			split = line.split('\t')
			pattern = [split[0].split(), split[1].split(), int(split[2]), split[3].strip()]
			pron_reached = False #variable to check if PRON has been reached, to know when to stop looking
			nouns = split[1].split() #duplicate of pattern[1] to delete out of containing all part of speech
			words = split[0].split() #duplicate of pattern[0] to delete out of containing all words
			for pos in pattern[1]:
				if pos == 'PRON' and pattern[3] == 'VERB_OWN': #variable only matters for this specific pattern
					pron_reached = True
					
				if (pos == 'NOUN' or pos == 'PROPN') and pron_reached == False:
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
								if pattern[3] != 'ZIJN_EV' and pattern[3] != 'ZIJN_MV' : #for this pattern, we need the first sequence of NOUNS, for the others we need te last. 
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
					#pronouns are being used for gender information. different patterns allow different sorts of words. pattern[3] is the type of pattern that found the NOUN and PRON.
					if pattern[0][pattern[1].index('PRON')] == 'hij' and pattern[3] == 'ZIJN_EV': 
						if noun in hij_zijn.keys():           		
							hij_zijn[noun] += pattern[2] #if a NOUN is already in the knowledge base, we update frequency
						else:
							hij_zijn.update({noun: pattern[2]})  # if a NOUN is new to the knowledge base, we add it

					elif pattern[0][pattern[1].index('PRON')] == 'hij' and pattern[3] == 'VERB_DAT':
						if noun in hij_dat.keys():            		
							hij_dat[noun] += pattern[2] 
						else:
							hij_dat.update({noun: pattern[2]})  

					elif pattern[0][pattern[1].index('PRON')] == 'zijn' and pattern[3] == 'CONJ':
						if noun in zijn_conj.keys():            		
							zijn_conj[noun] += pattern[2] 
						else:
							zijn_conj.update({noun: pattern[2]}) 

					elif pattern[0][pattern[1].index('PRON')] == 'zijn' and pattern[3] == 'VERB_DAT':
						if noun in zijn_dat.keys():            		
							zijn_dat[noun] += pattern[2] 
						else:
							zijn_dat.update({noun: pattern[2]}) 

					elif pattern[0][pattern[1].index('PRON')] == 'zijn' and pattern[3] == 'VERB_OWN':
						if noun in zijn_ww.keys():            		
							zijn_ww[noun] += pattern[2] 
						else:
							zijn_ww.update({noun: pattern[2]}) 
					#female
					elif pattern[0][pattern[1].index('PRON')] in ['zij', 'ze'] and pattern[3] == 'ZIJN_EV':
						if noun in zij_zijn.keys():            		
							zij_zijn[noun] += pattern[2] 
						else:
							zij_zijn.update({noun: pattern[2]}) 

					elif pattern[0][pattern[1].index('PRON')] == 'haar' and pattern[3] == 'CONJ':
						if noun in haar_conj.keys():            		
							haar_conj[noun] += pattern[2] 
						else:
							haar_conj.update({noun: pattern[2]})  

					elif pattern[0][pattern[1].index('PRON')] == 'haar' and pattern[3] == 'VERB_DAT':
						if noun in haar_dat.keys():            		
							haar_dat[noun] += pattern[2] 
						else:
							haar_dat.update({noun: pattern[2]})
 
					elif pattern[0][pattern[1].index('PRON')] == 'haar' and pattern[3] == 'VERB_OWN':
						if noun in haar_ww.keys():            		
							haar_ww[noun] += pattern[2] 
						else:
							haar_ww.update({noun: pattern[2]}) 
					#neutral
					elif pattern[0][pattern[1].index('PRON')] == 'het' and pattern[3] == 'ZIJN_EV':
						if noun in het_zijn.keys():            		
							het_zijn[noun] += pattern[2] 
						else:
							het_zijn.update({noun: pattern[2]}) 
  
					elif pattern[0][pattern[1].index('PRON')] == 'het' and pattern[3] == 'VERB_DAT':
						if noun in het_dat.keys():            		
							het_dat[noun] += pattern[2] 
						else:
							het_dat.update({noun: pattern[2]}) 
					#plural

					elif pattern[0][pattern[1].index('PRON')] == 'hun'  and pattern[3] == 'CONJ':
						if noun in hun_conj.keys():            		
							hun_conj[noun] += pattern[2] 
						else:
							hun_conj.update({noun: pattern[2]}) 

					elif pattern[0][pattern[1].index('PRON')] == 'hun'  and pattern[3] == 'VERB_DAT':
						if noun in hun_dat.keys():            		
							hun_dat[noun] += pattern[2] 
						else:
							hun_dat.update({noun: pattern[2]}) 
					elif pattern[0][pattern[1].index('PRON')] == 'hun'  and pattern[3] =='VERB_OWN':
						if noun in hun_ww.keys():            		
							hun_ww[noun] += pattern[2] 
						else:
							hun_ww.update({noun: pattern[2]}) 

					elif pattern[0][pattern[1].index('PRON')] == 'elkaars' and pattern[3] == 'VERB_OWN':
						if noun in elkaars_ww.keys():            		
							elkaars_ww[noun] += pattern[2] 
						else:
							elkaars_ww.update({noun: pattern[2]}) 
					elif pattern[0][pattern[1].index('PRON')] in ['zij', 'ze'] and pattern[3] == 'ZIJN_MV':
						if noun in plural_zijn.keys():            		
							plural_zijn[noun] += pattern[2] 
						else:
							plural_zijn.update({noun: pattern[2]}) 

	#print(hij_zijn['jongens'])  
	return [(hij_zijn, 'male'), (hij_dat, 'male'), (zijn_conj, 'male'), (zijn_dat, 'male'), (zijn_ww, 'male'), (zij_zijn, 'female'), (haar_conj, 'female'), (haar_dat, 'female'), (haar_ww, 'female'), (het_zijn, 'neutral'), (het_dat, 'neutral'), (hun_conj, 'plural'), (hun_dat, 'plural'), (hun_ww, 'plural'), (elkaars_ww, 'plural'), (plural_zijn, 'plural')]

	

def find_animacy(): #most comments for this function are equal to those of find_gender(), they can therefore be found over there. 
	#KB'S
	#animate
	wie_punct_adp = {}
	wie_adp = {}
	#inanimate
	welke_adp = {}
	welke_punct = {}
	welke_blank = {}
	welke_punct_adp = {}
	wat_punct = {}
	wat_blank = {}
	pickle_out = open("dict_animacy.pickle","wb")
	for i in range(0,12):
		filename_ani = '5gm-00'+str(i)+ '-annotated_animacy'
		file = open(filename_ani, 'r') 
		for line in file.readlines():
			position = None
			noun = ''
			split = line.split('\t')
			pattern = [split[0].split(), split[1].split(), int(split[2]), split[3].strip()]
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
						if pattern[0][pattern[1].index('PRON')] == 'wie' and pattern[3] == 'PUNCT-ADP':
							if noun in wie_punct_adp.keys():            		
								wie_punct_adp[noun] += pattern[2]
							else:
								wie_punct_adp.update({noun: pattern[2]}) 

						elif pattern[0][pattern[1].index('PRON')] == 'wie' and pattern[3] == 'ADP':
							if noun in wie_adp.keys():            		
								wie_adp[noun] += pattern[2]
							else:
								wie_adp.update({noun: pattern[2]}) 


						elif pattern[0][pattern[1].index('PRON')] == 'welke' and pattern[3] == 'PUNCT-ADP':
							if noun in welke_punct_adp.keys():            		
								welke_punct_adp[noun] += pattern[2]
							else:
								welke_punct_adp.update({noun: pattern[2]}) 

						elif pattern[0][pattern[1].index('PRON')] == 'welke' and pattern[3] == 'ADP':
							if noun in welke_adp.keys():            		
								welke_adp[noun] += pattern[2]
							else:
								welke_adp.update({noun: pattern[2]}) 

						elif pattern[0][pattern[1].index('PRON')] == 'welke' and pattern[3] == 'PUNCT':
							if noun in welke_punct.keys():            		
								welke_punct[noun] += pattern[2]
							else:
								welke_punct.update({noun: pattern[2]}) 

						elif pattern[0][pattern[1].index('PRON')] == 'welke' and pattern[3] == 'BLANK':
							if noun in welke_blank.keys():            		
								welke_blank[noun] += pattern[2]
							else:
								welke_blank.update({noun: pattern[2]}) 


						elif pattern[0][pattern[1].index('PRON')] == 'wat' and pattern[3] == 'PUNCT':
							if noun in wat_punct.keys():            		
								wat_punct[noun] += pattern[2]
							else:
								wat_punct.update({noun: pattern[2]}) 

						elif pattern[0][pattern[1].index('PRON')] == 'wat' and pattern[3] == 'BLANK':
							if noun in wat_blank.keys():            		
								wat_blank[noun] += pattern[2]
							else:
								wat_blank.update({noun: pattern[2]}) 
	return 	[(wie_punct_adp, 'animate'), (wie_adp, 'animate'), (welke_adp, 'inanimate'), (welke_punct, 'inanimate'), (welke_blank, 'inanimate'), (welke_punct_adp, 'inanimate'), (wat_punct, 'inanimate'), (wat_blank, 'inanimate')] 


	



def create_candidates(): #extracting words without annotation, to be annotated by the machine
	for i in range(1,24):
		file = open('Test/'+ str(i)+'_annotated' , 'r') 
		outfile = open('Test/'+ str(i)+'_words','w')
		lines = file.readlines()
		for line in lines:
			if len(line.split()) > 0:
				outfile.write(line.split('\t')[0] + '\n')
				
				
				
				
def check_KB_seperate(pattern_dict, conclusion): #the modified version op check_KB to work on the 

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
			if option1.lower() in pattern_dict.keys(): #first priority: the whole sequence of words (can also be a single word)
				outfile.write(option1 + '\t' + conclusion + '\n')

			else: 
				gender = 'Not in Knowledge Base'
				freq = 0 #this is to check if a match has been found
				for trigram in trigrams: #second priority: trying to match a trigram
					trigram = trigram.lower()
					if trigram in pattern_dict.keys():
						if pattern_dict[trigram] > freq: # if a match beats the certainty score of the previous match, it gets priority
							gender = conclusion
							freq = pattern_dict[trigram]

				if freq == 0:
					for bigram in bigrams:  #third priority: trying to match a bigram
						bigram = bigram.lower()
						if bigram in pattern_dict.keys():
							if pattern_dict[bigram] > freq:
								gender = conclusion
								freq = pattern_dict[bigram]
					if freq == 0: 
						line = line.split() 
						for unigram in line: #if nothing has been found, try to match single words. 
							word = unigram.lower()
							if word in pattern_dict.keys():
								if pattern_dict[word] > freq:
									gender = conclusion
									freq = pattern_dict[word]
				outfile.write(' '.join(line) + '\t' + gender + '\n')

def combine(KBS):
	combined_dict = {} #creating one big KB of words and their corresponding gender
	first = KBS.pop() #using one of the KBs as basis
	for key in first[0].keys():
		combined_dict.update({key: [first[1], first[0][key], first[0][key]]}) #converting information of first KB to the new format: gender, certainty, freq of gender
	for KB in KBS:
		dic = KB[0]
		for key in dic.keys():
			if key not in combined_dict.keys():
				combined_dict.update({key: [KB[1], dic[key], dic[key]]}) 
			else:
				if dic[key] > combined_dict[key][2]:
					if KB[1] == 'animate' and combined_dict[key][0] !='inanimate' and combined_dict[key][0] != 'animate': 
						pass #all genders are a more specific form of 'animate' and should therefore not be replace by that class
					else:
						combined_dict.update({key: [KB[1], dic[key]/combined_dict[key][2], dic[key]]}) #the most frequent class will be the final class
				elif dic[key] == combined_dict[key][2]:
					if KB[1] == 'animate' and combined_dict[key][0] !='inanimate':
						pass
					else:
						if KB[1] != combined_dict[key][0]:
							combined_dict.update({key: ['equal frequencies', 0, dic[key]]}) #if frequencies are the same, we can't specify a class. Certainty = 0.
				else: 
					if combined_dict[key][2]/dic[key] < combined_dict[key][1]:
						combined_dict[key][1] = (combined_dict[key][2]/dic[key]) #as a certainty measure, we will look at the distance between the most and second most frequent class.
	return combined_dict				
		

def combine_gender(KBS):
	male = {}
	female = {}
	plural = {}
	animate = {}
	inanimate = {} #creating one big KB of words and for every gender


	for KB in KBS:
		dic = KB[0]
		gender = KB[1]
		if gender == 'male': 
			for key in dic.keys():
				if key not in male.keys():
					male.update({key: dic[key]}) 
				else:
					male[key] += dic[key]
		if gender == 'female': 
			for key in dic.keys():
				if key not in female.keys():
					female.update({key: dic[key]}) 
				else:
					female[key] += dic[key]
		if gender == 'plural': 
			for key in dic.keys():
				if key not in plural.keys():
					plural.update({key: dic[key]}) 
				else:
					plural[key] += dic[key]
		if gender == 'animate': 
			for key in dic.keys():
				if key not in animate.keys():
					animate.update({key: dic[key]}) 
				else:
					animate[key] += dic[key]
		if gender == 'inanimate': 
			for key in dic.keys():
				if key not in inanimate.keys():
					inanimate.update({key: dic[key]}) 
				else:
					inanimate[key] += dic[key]
	return [(male,'male'), (female,'female'), (plural,'plural'), (animate, 'animate'), (inanimate, 'inanimate')] 	
	

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
				freq = 0 #this is the certainty measure calculated in the 'combine' function 
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
	words = [] #to check what words got classified wrong
	for i in range(1,24):
		human = open('Test/'+str(i)+'_annotated','r')
		machine = open('Test/'+str(i)+'_machine_annotation','r')
		for line in human.readlines():
			if len(line.split('\t')) >1:
				classifications_human.append(line.split('\t')[1].strip())
				words.append(line.split('\t')[0].strip())

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
	print('Male: ', (correct_male/381) *100,'%', '\n', 'Female: ', (correct_female/33)*100,'%', '\n', 'Neutral: ', (correct_neutral/170)*100,'%', '\n', 'Plural: ', (correct_plural/838)*100,'%', '\n', 'Inanimate: ', (correct_inanimate/2728)*100,'%', '\n', 'Not in KB: ', (not_in_KB/4150)*100,'%', '\n', 'Correct Animate: ', animate,' out of 1422', '\n\n')
	print('What went wrong?    (human annotation - machine annotation)')
	for pair in set(wrong_pairs):
		print(pair[0], ' - ', pair[1], ' : ', wrong_pairs.count(pair))








def main():
	KB_gender = find_gender()
	KB_animacy = find_animacy()
	candidates = create_candidates()
	KBS = KB_gender + KB_animacy
	KB_names = ['hij_zijn', 'hij_dat', 'zijn_conj', 'zijn_dat', 'zijn_ww', 'zij_zijn', 'haar_conj', 'haar_dat', 'haar_ww', 'het_zijn', 'het_dat', 'hun_conj', 'hun_dat', 'hun_ww', 'elkaars_ww', 'plural_zijn', 'wie_punct_adp', 'wie_adp', 'welke_adp', 'welke_punct', 'welke_blank', 'welke_punct_adp', 'wat_punct', 'wat_blank']  
	#The following four lines can be used to see the results for every pattern. They have been commented out here to avoid noise. 
	#for KB in KBS:
	#	print('\n', KB_names.pop(0)+': \n')
	#	check_KB_seperate(KB[0], KB[1]) 
	#	accuracy_test()
	#removing bad patterns
	KBS.pop(18) #remove((welke_adp, 'inanimate')) # results will still roll out for test set, but won't be taken into account
	KBS.pop(18)#remove((welke_punct, 'inanimate'))
	KBS.pop(18)#remove((welke_blank, 'inanimate'))
	KBS.pop(18)#remove((welke_punct_adp, 'inanimate'))
	KBS.pop(9) #remove((het_zijn, 'neutral'))
	KBS.pop(9) #remove((het_dat, 'neutral'))
	gender_KBS = combine_gender(KBS)
	KB_genders = ['male', 'female', 'plural', 'animate', 'inanimate']
	for KB in gender_KBS:
		print('\n', KB_genders.pop(0)+': \n')
		check_KB_seperate(KB[0], KB[1]) 
		accuracy_test()


	combined_dict = combine(gender_KBS)
	print('\n combined: \n ')
	check_KB(combined_dict)
	accuracy_test()


if __name__ == '__main__':
	main()

