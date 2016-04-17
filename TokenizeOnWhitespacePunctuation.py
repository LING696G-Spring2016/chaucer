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

