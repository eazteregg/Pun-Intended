import os
import re
import sys

from gensim.models.keyedvectors import KeyedVectors as kv
from nltk.metrics.distance import edit_distance

try:
    from nltk.corpus import cmudict
    from nltk.stem.wordnet import WordNetLemmatizer
except ImportError:
    print("Please make sure that 'pronouncing' and nltk for Python are installed and download cmudict using nltk.download()")

try:
    import pronouncing
except ImportError:
    print("Use pip install pronouncing")

MAX_EDIT_DISTANCE = 1

def lemmatize_list(lemmatizer, list1):
    list2 = [re.sub(r'[\'-]', r'', x) for x in list1]
    list2 = list(map(lambda x: lemmatizer.lemmatize(x), list2))
    return list2

# glove2word2vec helper methods
def myGet_glove_info(glove_file_name):
    """Return the number of vectors and dimensions in a file in GloVe format."""
    with open(glove_file_name, encoding='utf-8') as f:
        num_lines = sum(1 for line in f)
    with open(glove_file_name, encoding='utf-8') as f:
        num_dims = len(f.readline().split()) - 1
    return num_lines, num_dims

def myGlove2word2vec(glove_input_file, word2vec_output_file):
    """Convert `glove_input_file` in GloVe format into `word2vec_output_file in word2vec format."""
    num_lines, num_dims = myGet_glove_info(glove_input_file)
    if sys.version_info < (3,):
        with open(word2vec_output_file, 'wb', encoding='utf-8') as fout:
            fout.write("%s %s\n" % (num_lines, num_dims))
            with open(glove_input_file, 'rb', encoding='utf-8') as fin:
                for line in fin:
                    fout.write(line)
        return num_lines, num_dims
    else:
        with open(word2vec_output_file, 'w', encoding='utf-8') as fout:
            fout.write("%s %s\n" % (num_lines, num_dims))
            with open(glove_input_file, 'r', encoding='utf-8') as fin:
                for line in fin:
                    fout.write(line)
        return num_lines, num_dims


class SearchEngine:

    """This is the class that will handle all of the operations and queries and such"""

    def __init__(self, d_of_comparisons, vectorfile, combine, g2p_model, n_of_results=5, forcebin=True):

        self.d_of_comparisons = d_of_comparisons  # max dimensionality of the two lists
        self.n_of_results = n_of_results  # how many results the search engine is supposed to output
        self.combine = combine  # later to be implemented as choice between combination operations
        self.phondict = cmudict.dict()  # CMU Pronouncing Dictionary
        self.lemmatizer = WordNetLemmatizer()
        self.best_result = "no result" # Best word. big word. punny word.

        self.g2p_model = g2p_model

        # If vector file in gloVe format, transform it into word2vec and provide option to store it as binary

        create_bin = ''

        try:
            if vectorfile[-4:] == ".bin":
                binary = True
            elif forcebin:
                regex = r'(word2vec.)?' + vectorfile[:-4] + '.bin'
                for filename in os.listdir('data'):
                    if re.search(regex, filename):
                        print("Found binary file with the same name as the specified one. Will be loading the binary.")
                        vectorfile = filename
                        binary = True
                        break
                    binary = False
            else:
                binary = False

            print("Reading vectorfile...")
            self.word_vectors = kv.load_word2vec_format(os.path.join('data', vectorfile), binary=binary)  # retrieve word vectors from file

            if not binary and forcebin:

                while create_bin != 'y' and create_bin != 'n':
                    create_bin = input("Would you like to create a binary file for your vector file, so that future loading times may be shortened? y/n\n")

        except ValueError:
            print('Your vector file is not in the required word2vec format, conversion will be run...')
            print("Converting gloVe to word2vec format.-------------")

            while create_bin != 'y' and create_bin != 'n' and forcebin:

                create_bin = input("Would you like to create a binary file for your vector file, so that future loading times may be shortened? y/n\n")

            myGlove2word2vec(os.path.join('data', vectorfile), os.path.join('data', 'word2vec.' + vectorfile))
            self.word_vectors = kv.load_word2vec_format(os.path.join('data', 'word2vec.' + vectorfile))


        if create_bin == 'y':
            self.word_vectors.save_word2vec_format(os.path.join('data', 'word2vec.' + vectorfile[:-4] + '.bin'), binary=True)

    def get_phon_list(self, word, max_dist, ortho=None, rhyme=None):
        """Returns a list of phonetically similar words to word with max levenshtein distance of max_dist. If ortho is not
        None, the function will instead return a list of orthographically similar words."""

        if not ortho and not rhyme:  # Default case: Use CMU dict
            iterlist = self.phondict  # The list being iterated over is thus the CMU dict

            try:
                phon_rep = iterlist[word][0]  # CMU dict returns a list of pronunciations, thus [0]

            except KeyError:

                try:
                    print("use g2p for: " + word)
                    phon_rep = self.g2p_model.decode_word(word).split() #  This needs to be split because g2p returns a
                                                                        #  string
                except Exception:

                    print("Word not found in data bank!")

        elif ortho:  # If orthographic comparison is turned on, iterate over the CMU dict's keys instead
            iterlist = self.phondict.keys()  # which are simply orthographic words

        if not rhyme:  # If rhyme is turned on, skip the searching of the CMU dict
            results = []
            for x in iterlist:

                if not ortho:
                    pron_x = iterlist[x][0]

                    if pron_x == phon_rep:  # If the pronunciation of x is the same as word, it shouldn't be added to
                        continue            # the results, because we want phonetically similar words, not same ones

                    lvdist = edit_distance(pron_x, phon_rep)

                else:
                    lvdist = edit_distance(x, word)  # Simply check the orthographic edit_distance if ortho is True

                if lvdist <= max_dist:  # Add x from CMU dict to results, if its edit_distance to word is < max_dist
                    results.append((x, lvdist))
            
            results.sort(key=lambda x: x[0])    # Makes 'results' look similar each time and on different machines
            results.sort(key=lambda x: x[1])    # Sort the results by edit_distance
            return [x[0] for x in results[:self.d_of_comparisons]]

        else:  # If looking for rhymes, use pronouncing package to retrieve them
            results = pronouncing.rhymes(word)
            return results[:self.d_of_comparisons]

    def combines(self, asslist, phonlist, verbose=False):

        """Combines the associative list with the phonetic list. Using three types of possible combination methods
        as dictated by self.combine"""

        fn_combo = None
        if self.combine == 'sum':
            fn_combo = lambda m, n: m+n

        elif self.combine == 'prod':
            fn_combo = lambda m, n: (m+1)*(n+1)  # If either number is 0, the calculation is senseless

        if fn_combo:        # If either summation or multiplication has been chosen as combination method

            resdict = dict()
            lemmatized_phonlist = lemmatize_list(self.lemmatizer, phonlist)
            if verbose:
                print('Lemmatized Phonetic list:', lemmatize_list(self.lemmatizer, phonlist))

            for x in range(len(phonlist)):  # If a word is both in asslist and phonlist initialize its value with its place x in phonlist

                word = re.sub(r'\'', r'', phonlist[x])  # Get rid of single quotes as they don't affect pronunciation

                if phonlist[x] in asslist or self.lemmatizer.lemmatize(word) in asslist:  # Also check for the lemmatized version of word -> more likely to be found in asslist
                    resdict[phonlist[x]] = x
                else:                          # If the word is in neither list, initialize its value with a huge number
                    resdict[phonlist[x]] = 100000000 + x

            for y in range(len(asslist)):  # Now, for combining both lists, go the other way and check starting from asslist

                if asslist[y] in phonlist:  # If a word in its out-of-the-box form is found in phonlist, combine the scores
                    resdict[asslist[y]] = fn_combo(resdict[asslist[y]], y)

                elif asslist[y] in lemmatized_phonlist:  # If a word was not found in phonlist by default, try a lemmatized phonlist

                    index = lemmatized_phonlist.index(asslist[y]) # Find the first occurrence of the word
                    resdict[phonlist[index]] = fn_combo(resdict[phonlist[index]], y)  # combine

                else:                        # Otherwise it shouldn't be considered -> add a huge number!
                    resdict[asslist[y]] = 100000000 + y

        elif self.combine == 'inter':  # simply return the intersection of both lists
            return [x for x in asslist if x in phonlist]

        reslist = []

        for word in resdict:
            reslist.append((word, resdict[word]))  # Sort words by their respective score

        reslist.sort(key=lambda x: x[1])

        #self.best_result = [x for x in asslist if x in phonlist][0]
        if verbose:
            print([x for x in asslist if x in phonlist])

        return reslist[:self.n_of_results]

    def execute_query(self, soundslike, association, ortho, rhyme, verbose=False):
        """Method responsible for the execution of the main query. All of the other parts flow together in this."""

        try:
            ass_list = [x[0] for x in
                        self.word_vectors.most_similar(positive=[association], topn=self.d_of_comparisons)]
        except KeyError:
            return "Word %s not found in data bank." % association

        phon_list = self.get_phon_list(soundslike, MAX_EDIT_DISTANCE, ortho, rhyme)
        if verbose:
            print('Associations:\n', ass_list)
            print('Phonetically similar:\n', phon_list)

        result = self.combines(ass_list, phon_list)
        self.best_result = result[0][0]
        soundslike_lemma = self.lemmatizer.lemmatize(soundslike)
        best_result_lemma = self.lemmatizer.lemmatize(self.best_result)
        i = 0
        while i < len(result):
            if soundslike_lemma == best_result_lemma:
                self.best_result = result[i+1][0]
                break
            i += 1

        '''
        if len(result) > 1 and self.best_result == soundslike:
            self.best_result = result[1][0]'''
        print("best result: {}".format(self.best_result))
        return result

