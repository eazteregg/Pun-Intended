# -*- coding: utf-8 -*-
"""
Created on Thu May 25 19:55:45 2017

@author: Maximilian
"""
import argparse
import os
from nltk.metrics.distance import edit_distance

"""
# Get file paths to previously learned sentences and the function word list.
path_to_this_file = os.path.abspath(__file__) # i.e. /path/to/dir/implement_baseline.py
script_dir = os.path.split(path_to_this_file)[0] #i.e. /path/to/dir/
rel_path = "data/idiom_corpus_small.txt"
abs_corpus_path = os.path.join(script_dir, rel_path)

MAX_DISTANCE = 2  # Max edit distance to consider when exchanging words.

parser = argparse.ArgumentParser(description='Implement words in idioms')
# Required word argument
parser.add_argument('sounds_like', type=str,
                    help='sounds like x')

# Required word argument

# Optional edit distance argument
parser.add_argument('dist_arg', type=int, nargs='?',
                    help='An optional integer maximum edit distance argument')

args = parser.parse_args()
if args.dist_arg: MAX_DISTANCE = args.dist_arg

# The complete corpus, where every idiom has its explanation in the next line.
corpus = []  # 310
corpus_idioms = []  # Idioms only (155)
corpus_explanations = []  # Explanations only (155)

with open(abs_corpus_path, 'r') as corpus:
    corpus = [line.strip() for line in corpus if not line.startswith('#')]

corpus_idioms = corpus[0::2]
corpus_explanations = corpus[1::2]

# Get words from the user
x = args.sounds_like

# meaning = args.meaning
"""

# Implement word in sentence
class WordInsert():

    def __init__(self, sounds_like, corpus, verbose=False, max_distance=2):
        """

        :param sounds_like:
        :param corpus:
        :param verbose:
        :param max_distance:
        """
        self.sounds_like = sounds_like
        self.corpus = corpus
        self.verbose = verbose
        self.max_distance = max_distance
        self.sentences = []

    def insert_word(self):
        for line in self.corpus:
            for word in line.split():
                distance = edit_distance(self.sounds_like, word)
                if distance != 0 and distance <= self.max_distance:
                    sentence = line.replace(word, self.sounds_like)
                    self.sentences.append(sentence)

        if not self.sentences and self.max_distance < 5:
            print("No similar words to replace with edit distance {} found. Increasing edit distance by 1".format(self.max_distance))
            self.max_distance += 1
            self.insert_word()

        return self.sentences
