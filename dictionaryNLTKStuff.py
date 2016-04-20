import nltk
import os
import sys

m = input('Choose 0 for ntlk, 1 for Chaucer Glossary, 2 for Harvard Dict1, or 3 for Harvard Dict2: ')

mode = int(m)

def readFile(fileName):
	lines = []
	f = open(fileName, 'r')
	for line in f:
		lines.append(line)
	return lines

################## Begin NLTK Part ###################################

POSkey = {'RB':0,'VBP':1,'FW':2,'VBZ':3,'UH':4,'CD':5,'NNP':6,'NNP':7,
'VBD':8,'NN':9,'WP':10,'IN':11,'VB':12,'JJ':13,'NNS':14,'VBG':15,
'CC':16,'VBN':17,'DT':18,'EX':19,'JJR':20,'JJS':21,'LS':22,'MD':23,
'NNPS':24,'PDT':25,'POS':26,'PRP':27,'PRPS':28,'RBR':29,'RBS':30,
'RP':31,'SYM':32,'TO':33,'WDT':34,'WPS':35,'WRB':36}

def tagLines(lines):
	tagged = []
	modTagged = []
	count = 0
	for line in lines:
		if count % 2 == 0:
			words = nltk.word_tokenize(line)
			tags = nltk.pos_tag(words)
			for tag in tags:
				if tag not in tagged:
					tagged.append(tag)
		else:
			words = nltk.word_tokenize(line)
			tags = nltk.pos_tag(words)
			for tag in tags:
				if tag not in modTagged:
					modTagged.append(tag)	
		count = count + 1
	return tagged, modTagged

def formatDictionary(taggedLines, modTaggedLines):
	d = {}
	dM = {}
	for line in taggedLines:
		d[line[0]] = POSkey[line[1]]
	for line in modTaggedLines:
		dM[line[0]] = POSkey[line[1]]

	f = open('DictMid.txt','a')
	for key, value in d.items():
		f.write(str(key) + '\t' + str(value) + '\n')

	g = open('DictMod.txt','a')
	for key, value in dM.items():
		g.write(str(key) + '\t' + str(value) + '\n')

def makeDictionaryFromFile(fileName):
	lines = readFile(fileName)
	taggedLines, modTaggedLines = tagLines(lines)
	dictionary = formatDictionary(taggedLines, modTaggedLines)

##################### End of File Part, Begin Harvard1 and2 #########

def readOEDdict():
	lines = []
	f = open('outp.txt','r')
	for line in f:
		lines.append(line)
	return lines

def readHarvardDict():
	lines = []
	f = open('harvard.txt','r')
	for line in f:
		lines.append(line)
	return lines

def makeDict(lines):
	d = {}
	for line in lines:
		words = nltk.word_tokenize(line)
		if len(words) > 1:
			d[words[0]]=words[2]
	return d

###################### Begin Glossary Part #########################

def readGlossary():
	lines = []
	f = open('MEDictTxt.txt','r')
	for line in f:
		lines.append(line)
	return lines

def makeGlossDict(lines):
	POSdict = {'adv.': 0, 'verb, 2nd pers. prsnt. sg.': 1, 'FW': 2, 'comp.': 3, 
	'verb, 3rd prs. pst.': 4, 'interj.': 5, 'num.': 6, 'propernoun': 7, 
	'verb, 3rd prs. prsnt.': 8, 'phr.': 9, 'pro.': 10, 'verb, pst.': 11, 
	'noun, sg.': 12, 'question': 13, 'verb, 1st pers. prsnt. sg.': 14, 
	'prep.': 15, 'verb': 16, 'adj.': 17, 'verb, prsnt.': 18, 
	'verb, 3rd prs. sg.': 19, 'verb, 3rd prs. prsnt. sg.': 20, 'noun': 21, 
	'verb, prs. prtcpl.': 22, 'verb, pst.sg.': 23, 'verb, pst. sg.': 24, 
	'noun pl.': 25, 'conj.': 26, 'verb, 2nd prs. sg.': 27, 'verb, pst.pl.': 28, 
	'verb, pst. prtcpl.': 29,'noun, pl.':30}

	d = {}
	for line in lines:
		words = line.split('\t')
		d[words[0]] = POSdict[words[1]]
	return d

################## Begin writing dictionaries to files ###############

def FinalLookUp(data, dictionary):
	finalDictMid = {}
	finalDictMod = {}
	count = 0
	for d in data:
		words = nltk.word_tokenize(d)
		if count % 2 == 0:
			for word in words:
				if word not in finalDictMid.keys():
					if word in dictionary:
						finalDictMid[word] = dictionary[word]
					else:
						finalDictMid[word] = '0'
		else:
			for word in words:
				if word not in finalDictMod.keys():
					if word in dictionary:
						finalDictMod[word] = dictionary[word]
					else:
						finalDictMod[word] = '0'
		count = count + 1

	f = open('DictMid.txt','a')
	for key, value in finalDictMid.items():
		f.write(str(key) + '\t' + str(value) + '\n')

	g = open('DictMod.txt','a')
	for key, value in finalDictMod.items():
		g.write(str(key) + '\t' + str(value) + '\n')

################### See which version to do ###########################

def makeDictionaryFromOED(fileName):
	lines = readOEDdict()
	dictionary = makeDict(lines)
	data = readFile(fileName)
	taggedData = FinalLookUp(data, dictionary)

def makeDictionaryFromHarvard(fileName):
	lines = readHarvardDict()
	dictionary = makeDict(lines)
	data = readFile(fileName)
	taggedData = FinalLookUp(data, dictionary)

def makeDictionaryFromGlossary(fileName):
	lines = readGlossary()
	dictionary = makeGlossDict(lines)
	data = readFile(fileName)
	taggedData = FinalLookUp(data, dictionary)

if mode == 3:
	makeDictionaryFromOED(sys.argv[1])
elif mode == 2:
	makeDictionaryFromHarvard(sys.argv[1])
elif mode == 1:
	makeDictionaryFromGlossary(sys.argv[1])
else:
	makeDictionaryFromFile(sys.argv[1])