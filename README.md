# Pun-Intended
This software aids in pun generation, and other word-plays, like song lyrics and poetry.

### Dependencies
This project is written in python 3.5
Make sure that the follow dependencies are installed before trying to run Pun-Intended:
- nltk: `pip install --user -U nltk`
- cmudict corpus
    - To check/download cmudict, in the interperter type nltk.download() or from the command line: `python -m nltk.downloader cmudict`
- gensim
    - Make sure that gensim is installed and running. On Windows: This requires some workarounds. You will need numpy, mkl and scipy installed, which can be found at http://www.lfd.uci.edu/~gohlke/pythonlibs/. You may also need to install a c++ compiler. Installing gensim in Anaconda may be a good option (https://www.continuum.io/downloads)

### How to Run
1. Install the dependencies mentioned above
2. Clone the git to your local machine with `git clone https://github.com/eazteregg/Pun-Intended`
3. Download the vectors from the GloVe website (http://nlp.stanford.edu/data/glove.6B.zip), export and add `glove.6B.100d.txt` to the data folder.

### Command line Run options
- '--vecs' choose which glove text to build vectors from, default="glove.6B.100d.txt"
- '--combo' Choocse which method to compute distance default="sum", help="Combination method {sum|prod|inter}
- '--rhyme' Restricts to the phonological matches that rhyme to the input, default=true
- '--ortho' Uses orthographic matches instead of phonological ones, default=true
- '--expl'  Use explanations of idioms when building the pun, default = True
- '--sound_like' help="Specify 'sounds-like' word")
- '--means', help="Specify 'meaning' word")
- '--verbose', action="store_true", help="Print additional debugging info")
- '--func', action="store_true", help="Consider function words for replacement.")

-----------------------------------------------------------------------------------------------------------

Notes on the grapheme2phoneme fork:

NEEDS PYTHON2.7!

Sequitur G2P is a trainable data-driven grapheme-to-phoneme converter and may be used in this context to come up with phonetic representations for
strings not found in CMUdict. G2P is a Python 2 application, therefore, I tried wrapping it in Python 3 using subprocess.run(). To be frank, I
feel like it's more of a hack than a proper implementation, but it works for the time being.

1.
Download the latest (2016-04-25) Sequitur G2P from http://www-i6.informatik.rwth-aachen.de/web/Software/g2p.html
You will be needing Swig in order to build and run G2P, so download that as well using apt-get install.

2.
Follow the instructions found in the README file to build G2P
The g2pwrapper expects G2P to be located in the home folder, but you may change this in the source code with the PATH_G2P variable

G2P uses models trained on already transcribed words, like CMUdict. In order to train the model found in the data folder,
I split the CMU dict in half, taking only the odd numbered lines for training purposes and the even numbered ones for testing.
I went through 6 iterations of training, look at the G2P README to find out how. There might be further improvements to be had by continuing this, but
currently the model achieves a string accuracy of 57.74% and a symbol accuracy of 89.49%.


### Main.py
- takes command line arguments and parses them. 
- From these specifications, it then calls Search Engine.
- Model is created from the word vectors
- Creates the query menu
- After taking a query input, it calls search engine
- prints the words that are returned by search engine
- FindRelatedSentences is called with the model
- Filter Sentneces by topic id called on the FindRelatedSentences
- WordInsert is called on the filtered sentences with the best results from the search engine

### SearchEngine.py
- uses gensim
- uses edit distance (sum, prod, combination)
- lemmatize words

### test_searchEngine.py
- if you want to run the tests using a vector file in .txt format without being prompted for conversion to binary,
  switch the forcebin argument to False

### WordInsert.py
- insert best generated word into idioms
- ignore function words
- use a max edit distance of 1 if nothing increase to 2
- replace word based on rhyme
- 

### FindRelatedSentences.py
Finds the topics of 

### Remove Duplicates.py
- Removes duplicates from the idiom corpus.

### function_words.txt

### idiom_corpus.txt


<!---
From an older Version of readme:
When starting the program you may choose between the different vector models which are in text format out of the box.
As the loading of binary files is a lot faster, the program will prefer them over .txt files in case of there being a file with the same name, but .bin ending.
You will be offered to create a binary file corresponding to the .txt file you put in, unless there already is one.
-->
