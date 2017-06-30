# -*- coding: utf-8 -*-
"""
Created on Thu May 25 19:55:45 2017

@author: Maximilian
"""
import argparse
import os
from nltk.metrics.distance import edit_distance

# Get file paths to function words.
script_path = os.path.abspath(__file__) # i.e. /path/to/dir/WordInsert.py
script_dir = os.path.split(script_path)[0] #i.e. /path/to/dir/
rel_path = "data/function_words.txt"
rel_corpus_path="data/idiom_corpus.txt"
abs_file_path_function_words = os.path.join(script_dir, rel_path)
abs_file_path_idiom_corpus = os.path.join(script_dir, rel_corpus_path)

# Read the list of function words.
function_words = []
with open(abs_file_path_function_words, 'r', encoding="utf-8") as f:
    for line in f:
        function_words += line.split()

idiom = True
idiom_text = ""
idiom_explanation = dict()
with open(abs_file_path_idiom_corpus, 'r') as corpus:
    for line in corpus:
        if line.lstrip().startswith("#"): continue
        if idiom:
            idiom_text = line.strip().lower()
            idiom = False
        else:
            idiom_explanation[idiom_text] = line.strip().lower()
            idiom = True

# Implement word in sentence
class WordInsert():

    def __init__(self, sounds_like, reduced_corpus, verbose=False, max_distance=2, use_function_words=False, joke=False):
        """

        :param sounds_like:
        :param reduced_corpus:
        :param verbose:
        :param max_distance:
        """
        self.sounds_like = sounds_like
        self.corpus = reduced_corpus
        self.verbose = verbose
        self.max_distance = max_distance
        self.sentences = []
        self.use_function_words = use_function_words
        self.joke = joke
        self.recursion = False

    def insert_word(self):
        new_old_sentences = dict()
        for line in self.corpus:
            for word in line.split():
                if word in function_words and not self.use_function_words:
                    continue # ignore function words
                distance = edit_distance(self.sounds_like, word)
                if distance != 0 and distance <= self.max_distance:
                    sentence = line.replace(word, self.sounds_like)
                    if sentence not in self.sentences:
                        self.sentences.append(sentence)
                        new_old_sentences[sentence] = line

        if not self.sentences and self.max_distance < 3:
            print("No similar words to replace with edit distance {} found. \
                Increasing edit distance by 1".format(self.max_distance))
            self.max_distance += 1
            self.recursion = True
            self.insert_word()
            return self.sentences

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

        if self.joke:
            self.sentences = []
            for new, old in new_old_sentences.items():
                expl = idiom_explanation[old]

                if expl.endswith('.'):
                    expl = expl[:-1] + '?'
                else:
                    expl += '?'

                self.sentences += [expl]
                self.sentences += [new]
                self.sentences += ['']

            if not self.recursion:
                return self.sentences

        if not self.recursion:
            print("here")
            return self.sentences
