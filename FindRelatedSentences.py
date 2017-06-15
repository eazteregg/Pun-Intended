import os
import argparse
import operator
import gensim.scripts.glove2word2vec

from gensim.models.keyedvectors import KeyedVectors as kv

# Get file paths.
path_to_this_file = os.path.abspath(__file__)  # i.e. /path/to/dir/implement_baseline.py
script_dir = os.path.split(path_to_this_file)[0]  # C:.../Pun-Intended/
rel_path = "data/idiom_corpus_small.txt"
abs_corpus_path = os.path.join(script_dir, rel_path)  # C:.../Pun-Intended/data
bin_file_name = "word2vec.glove.6B.100d.bin"

abs_binary_path = os.path.join(script_dir, "data", bin_file_name)

with open(abs_corpus_path, 'r') as corpus:
    corpus = [line.strip().lower() for line in corpus if not line.startswith('#')]
    corpus_idioms = corpus[0::2]
    corpus_explanations = corpus[1::2]

"""
parser = argparse.ArgumentParser(description='Look for topic in sentences')
# Required topic argument
parser.add_argument('topic', type=str,
                    help='topic')

# Optional max result sentences argument
parser.add_argument('max_results', type=int, nargs='?',
                    help='determines how many sentences to return')

# Optional verbose argument for debug info
parser.add_argument('-v', "--verbose",
                    help='increase output verbosity', action="store_true")

args = parser.parse_args()
if args.topic: word = args.topic
max_results = 10
if args.max_results: max_results = args.max_results
"""


class FindRelatedSentences():
    """
    Given a word, chooses sentences in a corpus with related topic.
    E.g. given topic: "cat"
    Result: let the cat out of the bag
            curiosity killed the cat
            every dog has his day
            ...
    """

    def __init__(self, topic, model, verbose=False, max_results=10):
        self.topic = topic
        self.model = model
        self.verbose = verbose
        self.max_results = max_results
        self.word_dict = dict()
        self.score_dict = dict()
        self.sentences = []
        self.result_sentences = []


    def filter_sentences_by_topic(self):
        i = 0
        for sentence in corpus:
            self.sentences.append(sentence.split())
            self.word_dict[i] = sentence.split()
            i += 1

        def score(word, word_list, model):
            best_score = 0
            for word_in_list in word_list:
                try:
                    current_score = model.similarity(word, word_in_list)
                except KeyError:
                    continue
                if (current_score > best_score): best_score = current_score
            return best_score

        # Fill score_dict
        for key, value in self.word_dict.items():
            self.score_dict[key] = score(self.topic, value, self.model)

        top_sentences_and_scores = []
        top_sentences_and_scores = sorted(self.score_dict.items(), key=operator.itemgetter(1), reverse=True)[:self.max_results]

        if self.verbose:
            print(top_sentences_and_scores)

        for (key, value) in top_sentences_and_scores:
            if self.verbose:
                print(' '.join(self.word_dict[key]))
            #self.result_sentences += (self.word_dict[key])
            s = ""
            for word in self.word_dict[key]:
                s += word + " "
            self.result_sentences += [s.rstrip()]

        return self.result_sentences
