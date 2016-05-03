# Moses takes in two parallel files, one for each language, with one sentence per line. This script converts files
# to this format. Use this by dumping all of the files you want merged into Moses-compatible corpus files (keep in
# mind that you should withhold test data) into a single directory, then running:
#
# python moses_convert.py directory
#
# Use the tokenized data for this or else the sparsity problem will be even worse.
#
# IMPORTANT! Make sure you delete or move the output files each time you want to start over. If these files already
# exist when you invoke this program they will simply have more sentences appended to them.

import os
import sys


def split(filename):
    middle_sents = []
    modern_sents = []
    with open(filename, 'r') as f:
        count = 0
        for line in f:
            if count % 2 == 0:
                modern_sents.append(line)
            else:
                middle_sents.append(line)
            count += 1

    middle_sents = list(sent for sent in middle_sents if sent)
    modern_sents = list(sent for sent in modern_sents if sent)
    return middle_sents, modern_sents


def merge_append(filename, middle, modern):
    filename_en = filename + ".en"
    filename_me = filename + ".me"

    with open(filename_en, 'a') as f:
        for sentence in modern:
            print(sentence, end="", file=f)
    with open(filename_me, 'a') as f:
        for sentence in middle:
            print(sentence, end="", file=f)


if not sys.argv[1]:
    directory = "."
else:
    directory = sys.argv[1]

for dirpath, dirnames, filenames in os.walk(directory):
    for name in filenames:
        path = os.path.join(dirpath, name)
        print("Processing " + path)
        me, en = split(path)
        merge_append("chaucer_merged", me, en)
