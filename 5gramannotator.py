#!/usr/bin/env python3
import spacy


def POS_TAG(nlp):
	file = open('test2', 'r') 
	outfile = open('test2-annotated','a')
	i = 0
	for line in file.readlines():
		i += 1
		print(i)
		line = line.split('\t') 
		line_int = int(line[1])
		if line_int > 60:	
			tag = nlp(line[0])
			text = ''
			pos = ''
			for token in tag:
				text += token.text.lower() + ' '
				pos += str(token.pos_) + ' '
			outfile.write(text + '\t' + pos + '\t' + str(line_int)+'\n')
		else:
			pass
	
	outfile.close()

                

                 
def main():
	nlp = spacy.load('nl_core_news_sm')
	POS_TAG(nlp)
if __name__ == '__main__':
	main()

