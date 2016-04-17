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
        self.stringToTokenize = re.sub(r"(\w)('\w)", r"\1 \2", self.stringToTokenize)
        unfileredUnigrams = re.findall(r"[\w']+", self.stringToTokenize)
        for word in unfileredUnigrams:
            self.unigrams.append(str(word))
        return self.unigrams

