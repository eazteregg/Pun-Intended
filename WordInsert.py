# -*- coding: utf-8 -*-
"""
Created on Thu May 25 19:55:45 2017

@author: Maximilian
"""
import argparse
import os
from nltk.metrics.distance import edit_distance

# Implement word in sentence
class WordInsert():


    def __init__(self, sounds_like, corpus, verbose=False, max_distance=1):
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

        if not self.sentences and self.max_distance < 3:
            print("No similar words to replace with edit distance {} found. "
                  "Increasing edit distance by 1".format(self.max_distance))
            self.max_distance += 1
            self.insert_word()

        return self.sentences
