import gensim
from levenshtein import levenshtein
from gensim.models.keyedvectors import KeyedVectors as kv
import sys


class SearchEngine():
    """This is the class that will handle all of the operations and queries and such"""

    def __init__(self, d_of_comparisons, n_of_results=5, combine='s'):

        self.d_of_comparisons = d_of_comparisons  # max dimensionality of the two lists
        self.n_of_results = n_of_results  # how many resutlts the search engine is supposed to outpu
        self.combine = combine  # later to be implemented as choice between combination operations
        self.word_vectors = kv.load_word2vec_format('data/glove.6B.100d.txt')  # retrieve word vectors from file
        self.phondict = dict()

        # Fill the phonetic dictionary
        with open('data/cmudict-0.7b.utf8') as phondict:
            for line in phondict:
                if line[:3] == ";;;":
                    continue

                line = line.split(maxsplit=1)
                #print(line[0], line[1])
                self.phondict[line[0].lower()] = line[1]

    def get_phon_list(self, word, max_dist):
        """Returns a list of phonetically similar words to word with max levenshtein distance of max_dist"""
        try:
            phon_rep = self.phondict[word]

        except KeyError:
            print("Word not found in data bank!")

        results = []
        for x in self.phondict:
            lvdist = levenshtein(self.phondict[x].split(), phon_rep.split())

            if lvdist <= max_dist:
                results.append((x, lvdist))

        results.sort(key=lambda x: x[1])
        return [x[0] for x in results[:self.d_of_comparisons]]

    def combines(self, ass_list, phonlist, fn_combo=lambda x, y: x + y):

        """Combines the associative list with the phonetic list. To be implemented: fn_combo which steers the 
        combination operation"""

        # if len(ass_list) != len(phonlist):                            # The way this is implemented, this is not...

        # raise ValueError("listA must have the same length as listB!") # ...required

        resdict = dict()
        for x in range(len(ass_list)):
            if ass_list[x] in phonlist:
                resdict[ass_list[x]] = x
            else:
                resdict[ass_list[x]] = 100000000 + x
        for y in range(len(phonlist)):
            try:
                resdict[phonlist[y]] += y
            except KeyError:
                resdict[phonlist[y]] = 100000000 + y

        reslist = []
        for word in resdict:
            reslist.append((word, resdict[word]))
        reslist.sort(key=lambda x: x[1])
        print([x for x in ass_list if x in phonlist])
        return reslist[:self.n_of_results]
        # return [x[0] for x in reslist[:self.n_of_results]]

    def execute_query(self, soundslike, association):

        ass_list = [x[0] for x in
                    self.word_vectors.most_similar(positive=[association], topn=self.d_of_comparisons)]
        phon_list = self.get_phon_list(soundslike, 2)

        return self.combines(ass_list, phon_list)



