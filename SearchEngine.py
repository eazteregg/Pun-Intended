import os

import gensim.scripts.glove2word2vec
from gensim.models.keyedvectors import KeyedVectors as kv
from nltk.corpus import cmudict
from nltk.metrics.distance import edit_distance


class SearchEngine():
    """This is the class that will handle all of the operations and queries and such"""

    def __init__(self, d_of_comparisons, vectorfile, n_of_results=5, combine='s'):

        self.d_of_comparisons = d_of_comparisons  # max dimensionality of the two lists
        self.n_of_results = n_of_results  # how many results the search engine is supposed to output
        self.combine = combine  # later to be implemented as choice between combination operations
        self.phondict = cmudict.dict()  # CMU Pronouncing Dictionary

        # If vector file in gloVe format, transform it into word2vec and provides option to store it as binary

        create_bin = 'n'

        try:
            if vectorfile[-4:] == ".bin":
                binary = True
            else:
                for filename in os.listdir('data'):
                    if filename == 'word2vec.' + vectorfile[:-4] + '.bin':
                        print("Found binary file with the same name as the specified one. Will be loading the binary.")
                        vectorfile = filename
                        binary = True
                        break
                    binary = False

            self.word_vectors = kv.load_word2vec_format(os.path.join('data', vectorfile), binary=binary)  # retrieve word vectors from file

            if not binary:
                create_bin = input("Would you like to create a binary file for your vector file, so that future loading times may be shortened? y/n\n")

        except ValueError as v:
            print(v)
            print("Converting gloVe to word2vec format.-------------")

            create_bin = input("Would you like to create a binary file for your vector file, so that future loading times may be shortened? y/n\n")

            gensim.scripts.glove2word2vec.glove2word2vec(os.path.join('data', vectorfile), os.path.join('data', 'word2vec.' + vectorfile))
            self.word_vectors = kv.load_word2vec_format(os.path.join('data', 'word2vec.' + vectorfile))

        if create_bin == 'y':
            self.word_vectors.save_word2vec_format(os.path.join('data', 'word2vec.' + vectorfile[:-4] + '.bin'), binary=True)

    def get_phon_list(self, word, max_dist):
        """Returns a list of phonetically similar words to word with max levenshtein distance of max_dist"""
        try:

            phon_rep = self.phondict[word][0]  # CMU dict returns a list of pronunciations, thus [0]
            print(phon_rep)
        except KeyError:
            print("Word not found in data bank!")

        results = []
        for x in self.phondict:
            pron_x = self.phondict[x][0]
            lvdist = edit_distance(pron_x, phon_rep)

            if lvdist <= max_dist:
                results.append((x, lvdist))

        results.sort(key=lambda x: x[1])
        return [x[0] for x in results[:self.d_of_comparisons]]

    def combines(self, ass_list, phonlist):

        """Combines the associative list with the phonetic list. To be implemented: fn_combo which steers the 
        combination operation"""

        fn_combo = None
        if self.combine == 'sum':
            fn_combo = lambda m, n: m+n

        elif self.combine == 'prod':
            fn_combo = lambda m, n: (m+1)*(n+1)  # If either number is 0, the calculation is senseless

        if fn_combo:        # If either summation or multiplication has been chosen as combination method

            resdict = dict()

            for x in range(len(ass_list)):

                if ass_list[x] in phonlist:  # If a word is in ass_list and phonlist initialize its value with x
                    resdict[ass_list[x]] = x
                else:                        # Otherwise it shouldn't be considered -> add a huge number!
                    resdict[ass_list[x]] = 100000000 + x

            for y in range(len(phonlist)):

                try:                # Now for all words in phonlist combine their place with whats already in resdict
                    resdict[phonlist[y]] = fn_combo(resdict[phonlist[y]], y)
                except KeyError:    # If it is not already in resdict, it shouldn't be considered -> add a huge number!
                    resdict[phonlist[y]] = 100000000 + y

        elif self.combine == 'inter':  # simply return the intersection of both lists
            return [x for x in ass_list if x in phonlist]

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



