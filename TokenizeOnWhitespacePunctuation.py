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
        self.stringToTokenize = re.sub(r"\s'|'\s|'$", "", self.stringToTokenize)
        self.stringToTokenize = re.sub(r"(\w)('\w)", r"\1 \2", self.stringToTokenize)
        unfilteredUnigrams = re.findall(r"[\w']+", self.stringToTokenize)
        for word in unfilteredUnigrams:
            self.unigrams.append(word)
        return self.unigrams
