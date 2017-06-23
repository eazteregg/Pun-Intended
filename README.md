# readme for Pun-Intended project
The goal of this project is to aid in pun generation.

### Specifications
This project is written in python 3.5

### Dependencies
Make sure that the follow dependencies are installed before trying to run Pun-Intended:
- nltk
- cmudict corpus
    - To check/download cmudict, in the interperter type nltk.download() or from the command line: `python -m nltk.downloader cmudict`
- gensim
    - Make sure that gensim is installed and running. On Windows: This requires some workarounds. You will need numpy, mkl and scipy installed, which can be found at http://www.lfd.uci.edu/~gohlke/pythonlibs/. You may also need to install a c++ compiler. Installing gensim in Anaconda may be a good option (https://www.continuum.io/downloads)

### How to Run
1.  Install the dependencies mentioned above
2. clone the git to your local machine with `git clone https://github.com/eazteregg/Pun-Intended`


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

### TestSearchEngine.py

### WordInsert.py
- insert best generated word into idioms
- ignore function words
- use a max edit distance of 1 if nothing increase to 2
- replace word based on rhyme
- 

### FindRelatedSentences.py
Finds the topics of 

### Remove Duplicates.py
Removes duplicates from the 

### function_words.txt

### idiom_corpus.txt

# When starting the program you may choose between the different vector models which are in text format out of the box.
# As the loading of binary files is a lot faster, the program will prefer them over .txt files in case of there being a file with the same name, but .bin ending.
# You will be offered to create a binary file corresponding to the .txt file you put in, unless there already is one.
