# -*- coding: utf-8 -*-
"""
Created on Thu May 25 19:55:45 2017

@author: Maximilian
"""
import argparse
import string
import os
from nltk.metrics.distance import edit_distance
try:
    from nltk.corpus import cmudict
    from nltk.tokenize import wordpunct_tokenize
except ImportError:
    print("Please make sure that 'pronouncing' and nltk for Python are installed and download cmudict using nltk.download()")
try:
    import pronouncing
except ImportError:
    print("Use: pip install pronouncing")

# Get file paths to function words.
script_path = os.path.abspath(__file__) # i.e. /path/to/dir/WordInsert.py
script_dir = os.path.split(script_path)[0] #i.e. /path/to/dir/
rel_path = "data/function_words.txt"
abs_file_path_function_words = os.path.join(script_dir, rel_path)

# Read the list of function words.
function_words = []
with open(abs_file_path_function_words, 'r', encoding="utf-8") as f:
    for line in f:
        function_words += line.split()

# Implement word in sentence
class WordInsert():

    def __init__(self, sounds_like, corpus, g2p_model, verbose=False, max_distance=2, use_function_words=False):
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
        self.use_function_words = use_function_words
        self.cmudict = cmudict.dict()
        self.cmuextension = {}
        self.g2p_model = g2p_model

    def insert_word(self, ortho=False, rerun=False):
        for line in self.corpus:
            for word in wordpunct_tokenize(line):
                if (word in function_words and not self.use_function_words) or word in string.punctuation:
                    continue  # ignore function words and punctuation
                if ortho:
                    distance = edit_distance(self.sounds_like, word)
                else:
                    try:  # Try to find phonetic representation in cmudict
                        phonrep1 = self.cmudict[self.sounds_like][0]
                    except KeyError:  # If it is not in there, do the following:
                        if rerun:     # If this is is a recursive rerun, as called at the end of this function
                            phonrep1 = self.cmuextension[self.sounds_like]  # Load the representation as computed previously
                        else:       # If this is the first run, use g2p to transcribe and save it in cmuextension.
                            phonrep1 = self.g2p_model.decode_word((self.sounds_like))
                            self.cmuextension[self.sounds_like] = phonrep1
                            if self.verbose:
                                print(self.sounds_like, phonrep1)
                    try:  # Try to find phonetic representation in cmudict
                        phonrep2 = self.cmudict[word][0]
                    except KeyError:    # If not in there follow the steps as described above
                        if rerun:
                            phonrep2 = self.cmuextension[word]
                        else:
                            phonrep2 = self.g2p_model.decode_word(word)
                            self.cmuextension[word] = phonrep2
                            if self.verbose:
                                print(word, phonrep2)

                    distance = edit_distance(phonrep1, phonrep2)

                if distance != 0 and distance <= self.max_distance:
                    sentence = line.replace(word, self.sounds_like)
                    if sentence not in self.sentences:
                        self.sentences.append(sentence)

        if not self.sentences and self.max_distance < 3:
            print("No similar words to replace with edit distance {} found. \
                Increasing edit distance by 1".format(self.max_distance))
            self.max_distance += 1
            self.insert_word(rerun=True)

        elif not self.sentences:
            print("No similar words to replace with edit distance {} found. ".format(self.max_distance))
            print("Do you want to keep going? The quality of the results will probably be bad.")
            while True:
                user_input = input("(y/n)\n")
                if (user_input == 'y'):
                    self.max_distance += 1
                    self.insert_word()
                    break
                elif (user_input == 'n'):
                    break

        return self.sentences
