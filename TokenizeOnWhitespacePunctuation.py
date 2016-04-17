import re
from Classes.StopwordsList import StopwordsList


class TokenizeOnWhitespacePunctuation(object):
    def __init__(self, stringToTokenize, applyStopwords=False, keepCaps=False):
        self.keepCaps = keepCaps
        self.applyStopwords = applyStopwords

        if self.keepCaps:
            self.stringToTokenize = stringToTokenize
        else:
            self.stringToTokenize = stringToTokenize.lower()

        self.listOfStopwords = StopwordsList.stopwords()

        self.unigrams = []
        self.bigrams = []
        self.bothUnigramsBigrams = []

    def removeUrls(self):
        self.stringToTokenize = re.sub('\w+\.\w+', '', self.stringToTokenize)

    def getUnigrams(self):
        self.unigrams = []
        self.removeUrls()
        unfileredUnigrams = re.findall(r"[\w']+", self.stringToTokenize)
        for word in unfileredUnigrams:
            if self.applyStopwords == True:
                if word not in self.listOfStopwords:
                    self.unigrams.append(word)
            else:
                self.unigrams.append(word)
        return self.unigrams

    def getBigrams(self):
        self.bigrams = []
        self.getUnigrams()
        for i in range(len(self.unigrams) - 1):
            currentToken = self.unigrams[i]
            nextToken = self.unigrams[i + 1]
            bigram = '%s %s' % (currentToken, nextToken)
            self.bigrams.append(bigram)
        return self.bigrams

    def getBothUnigramsBigrams(self):
        self.getUnigrams()
        self.getBigrams()
        self.bothUnigramsBigrams = self.unigrams[:]
        for i in self.bigrams:
            self.bothUnigramsBigrams.append(i)
        return self.bothUnigramsBigrams
