import os

import gensim.scripts.glove2word2vec
import re
from gensim.models.keyedvectors import KeyedVectors as kv
try:
    import pronouncing
    from nltk.corpus import cmudict
    from nltk.metrics.distance import edit_distance
    from nltk.stem.wordnet import WordNetLemmatizer
except ImportError:
    print("Please make sure that 'pronouncing' and nltk for Python are installed and download cmudict using nltk.download()")

MAX_EDIT_DISTANCE = 1

def lemmatize_list(lemmatizer, list1):
    list2 = [re.sub(r'[\'-]', r'', x) for x in list1]
    list2 = list(map(lambda x: lemmatizer.lemmatize(x), list2))
    return list2

class SearchEngine():
    """This is the class that will handle all of the operations and queries and such"""

    def __init__(self, d_of_comparisons, vectorfile, combine, n_of_results=5):

        self.d_of_comparisons = d_of_comparisons  # max dimensionality of the two lists
        self.n_of_results = n_of_results  # how many results the search engine is supposed to output
        self.combine = combine  # later to be implemented as choice between combination operations
        self.phondict = cmudict.dict()  # CMU Pronouncing Dictionary
        self.lemmatizer = WordNetLemmatizer()

        # If vector file in gloVe format, transform it into word2vec and provides option to store it as binary

        create_bin = ''

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

                while create_bin != 'y' and create_bin != 'n':
                    create_bin = input("Would you like to create a binary file for your vector file, so that future loading times may be shortened? y/n\n")

        except ValueError as v:
            print('Your vector file is not in the required word2vec format, conversion will be run...')
            print("Converting gloVe to word2vec format.-------------")

            while create_bin != 'y' and create_bin != 'n':

                create_bin = input("Would you like to create a binary file for your vector file, so that future loading times may be shortened? y/n\n")

            gensim.scripts.glove2word2vec.glove2word2vec(os.path.join('data', vectorfile), os.path.join('data', 'word2vec.' + vectorfile))
            self.word_vectors = kv.load_word2vec_format(os.path.join('data', 'word2vec.' + vectorfile))

        if create_bin == 'y':
            self.word_vectors.save_word2vec_format(os.path.join('data', 'word2vec.' + vectorfile[:-4] + '.bin'), binary=True)

    def get_phon_list(self, word, max_dist, ortho=None, rhyme=None):
        """Returns a list of phonetically similar words to word with max levenshtein distance of max_dist. If ortho is not
        None, the function will instead return a list of orthographically similar words."""


        if not ortho and not rhyme:
            iterlist = self.phondict
            try:

                phon_rep = iterlist[word][0]  # CMU dict returns a list of pronunciations, thus [0]
                print(phon_rep)
            except KeyError:
                print("Word not found in data bank!")

        elif ortho:
            iterlist = self.phondict.keys()

        if not rhyme:
            results = []
            for x in iterlist:

                if not ortho:
                    pron_x = iterlist[x][0]
                    lvdist = edit_distance(pron_x, phon_rep)

                else:
                    lvdist = edit_distance(x, word)

                if lvdist <= max_dist:
                    results.append((x, lvdist))

            results.sort(key=lambda x: x[1])
            return [x[0] for x in results[:self.d_of_comparisons]]

        else:
            results = pronouncing.rhymes(word)
            return results[:self.d_of_comparisons]

    def combines(self, ass_list, phonlist):

        """Combines the associative list with the phonetic list. To be implemented: fn_combo which steers the 
        combination operation"""

        fn_combo = None
        if self.combine == 'sum':
            fn_combo = lambda m, n: m+n

        elif self.combine == 'prod':
            fn_combo = lambda m, n: (m+1)*(n+1) # If either number is 0, the calculation is senseless

        if fn_combo:        # If either summation or multiplication has been chosen as combination method

            resdict = dict()

            for x in range(len(phonlist)):

                word = phonlist[x].replace('\'', '')
                if phonlist[x] in ass_list or self.lemmatizer.lemmatize(word) in ass_list:
                    resdict[phonlist[x]] = x
                else:
                    resdict[phonlist[x]] = 100000000 + x

            for y in range(len(ass_list)):

                if ass_list[y] in phonlist:  # If a word is in ass_list and phonlist initialize its value with x
                    resdict[ass_list[y]] = fn_combo(resdict[ass_list[y]], y)

                elif ass_list[y] in lemmatize_list(self.lemmatizer, phonlist): # If a word was not found in phonlist by default, try a lemmatized phonlist
                    print(lemmatize_list(self.lemmatizer, phonlist))
                    index = lemmatize_list(self.lemmatizer, phonlist).index(ass_list[y])
                    resdict[phonlist[index]] = fn_combo(resdict[phonlist[index]], y)

                else:                        # Otherwise it shouldn't be considered -> add a huge number!
                    resdict[ass_list[y]] = 100000000 + y

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

    def execute_query(self, soundslike, association, ortho, rhyme):

        try:
            ass_list = [x[0] for x in
            self.word_vectors.most_similar(positive=[association], topn=self.d_of_comparisons)]
        except KeyError:
            return "Word %s not found in databank." % association

        phon_list = self.get_phon_list(soundslike, MAX_EDIT_DISTANCE, ortho, rhyme)
        print(ass_list)
        print(phon_list)

        return self.combines(ass_list, phon_list)



