# -*- coding: utf-8 -*-
"""
Created on Thu May 25 19:55:45 2017

@author: Maximilian
"""
import argparse
from nltk.metrics.distance import edit_distance

MAX_DISTANCE = 2  # Max edit distance to consider when exchanging words.

parser = argparse.ArgumentParser(description='Implement words in idioms')
# Required word argument
parser.add_argument('sounds_like', type=str,
                    help='sounds like x')

# Required word argument
"""
parser.add_argument('meaning', type=str,
                    help='meaning associated with y')"""

# Optional edit distance argument
parser.add_argument('dist_arg', type=int, nargs='?',
                    help='An optional integer maximum edit distance argument')

args = parser.parse_args()
if args.dist_arg: MAX_DISTANCE = args.dist_arg

# The complete corpus, where every idiom has its explanation in the next line.
corpus = []  # 310
corpus_idioms = []  # Idioms only (155)
corpus_explanations = []  # Explanations only (155)

with open('data/idiom_corpus_small.txt', 'r') as corpus:
    corpus = [line.strip() for line in corpus if not line.startswith('#')]

corpus_idioms = corpus[0::2]
corpus_explanations = corpus[1::2]

# Get words from the user
x = args.sounds_like

# meaning = args.meaning

# Implement word in sentence

sentences = []
for line in corpus_idioms:
    for word in line.split():
        distance = edit_distance(x, word)
        if distance != 0 and distance <= MAX_DISTANCE:
            sentence = line.replace(word, x)
            sentences.append(sentence)

print(sentences)
