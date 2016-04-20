import os
import re
from TokenizeOnWhitespacePunctuation import TokenizeOnWhitespacePunctuation


def tokenize_raw(filename):
    # Open input and output files, creating output file as necessary
    infile = open(filename, 'r')
    outfilename = str(os.getcwd()) + "/" + re.sub("raw", "tokenized", str(filename))
    print("Writing", outfilename)
    os.makedirs(os.path.dirname(outfilename), exist_ok=True)
    outfile = open(outfilename, 'w')

    for line in infile:
        tokenizer = TokenizeOnWhitespacePunctuation(line)
        tokenized = tokenizer.getUnigrams()
        print(' '.join(tokenized), file=outfile)

    infile.close()
    outfile.close()
    return


for dirpath, dirnames, filenames in os.walk('data/raw'):
    for name in filenames:
        tokenize_raw(os.path.join(dirpath, name))
