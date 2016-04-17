import re

knight = 'knight0001-0034.txt' #put filepath here

def clean(files):
	text = open(files, 'r')
	text = text.read()
	text = re.sub(r'\.|-|;|,|\'|:', '', text) #delete punctuation

	text = text.splitlines() 
	for words in text:
		clean_text = words.lower() #lowercase
		print(clean_text) #prints cleaned text

clean(knight)
