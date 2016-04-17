import re


class TokenizeOnWhitespacePunctuation(object):
    def __init__(self, stringToTokenize, keepCaps=False):
        self.keepCaps = keepCaps

        if self.keepCaps:
            self.stringToTokenize = stringToTokenize
        else:
            self.stringToTokenize = stringToTokenize.lower()

        self.unigrams = []

    def getUnigrams(self):
        self.unigrams = []
        unfileredUnigrams = re.findall(r"[\w']+", self.stringToTokenize)
        for word in unfileredUnigrams:
            self.unigrams.append(word)
        return self.unigrams