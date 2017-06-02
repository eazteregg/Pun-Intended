import gensim.scripts.glove2word2vec
from levenshtein import levenshtein
from gensim.models.keyedvectors import KeyedVectors as kv
import os


class SearchEngine():
    """This is the class that will handle all of the operations and queries and such"""

    def __init__(self, d_of_comparisons, vectorfile, n_of_results=5, combine='s'):

        self.d_of_comparisons = d_of_comparisons  # max dimensionality of the two lists
        self.n_of_results = n_of_results  # how many resutlts the search engine is supposed to output
        self.combine = combine  # later to be implemented as choice between combination operations

        #If vector file in gloVe format, tranfsorm it into word2vec and provides option to store it as binary

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

        self.phondict = dict()

        # Fill the phonetic dictionary
        with open(os.path.join('data', 'cmudict-0.7b.utf8')) as phondict:
            for line in phondict:
                if line[:3] == ";;;":   #skip the first couple of lines
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

    def combines(self, ass_list, phonlist):

        """Combines the associative list with the phonetic list. To be implemented: fn_combo which steers the 
        combination operation"""

        # if len(ass_list) != len(phonlist):                            # The way this is implemented, this is not...

        # raise ValueError("listA must have the same length as listB!") # ...required

        fn_combo = None
        if self.combine == 's':
            fn_combo = lambda m, n: m+n

        elif self.combine == 'p':
            fn_combo = lambda m, n: (m+1)*(n+1) # If either number is 0, the calculation is senseless

        if fn_combo:        #If either summation or multiplication has been chosen as combination method

            resdict = dict()
            for x in range(len(ass_list)):
                if ass_list[x] in phonlist:
                    resdict[ass_list[x]] = x
                else:
                    resdict[ass_list[x]] = 100000000 + x
            for y in range(len(phonlist)):
                try:
                    resdict[phonlist[y]] = fn_combo(resdict[phonlist[y]], y)
                except KeyError:
                    resdict[phonlist[y]] = 100000000 + y

        else:               #If nothing has been chosen -> default to intersection

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



