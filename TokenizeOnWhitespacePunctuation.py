import re


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

    def getUnigrams(self):
        self.unigrams = []
        unfileredUnigrams = re.findall(r"[\w']+", self.stringToTokenize)
        for word in unfileredUnigrams:
            if self.applyStopwords == True:
                if word not in self.listOfStopwords:
                    self.unigrams.append(word)
            else:
                self.unigrams.append(word)
        return self.unigrams