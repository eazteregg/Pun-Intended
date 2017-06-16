# Pun-Intended
An application designed to help users find puns. Still in development.

Notes on how to get the program to work:

0. Make sure that `nltk` is installed in Python, and that the cmudict corpus is installed. 
(To check/download cmudict, in the interperter type `nltk.download()` or from the command line: `python -m nltk.downloader cmudict`)

  Make sure that `gensim` is installed and running. 
On Windows: This requires some workarounds. You will need numpy, mkl and scipy installed, which can be found at http://www.lfd.uci.edu/~gohlke/pythonlibs/. You may also need to install a c++ compiler.
Installing `gensim` in Anaconda may be a good option (https://www.continuum.io/downloads)

1. Download the GloVe 6B Vectors based on the Wikipedia2014 and Gigaword5 corpus. 
Official website: https://nlp.stanford.edu/projects/glove/
Direct download: http://nlp.stanford.edu/data/glove.6B.zip
Unzip and add the file **glove.6B.100d.txt** to the data folder.

2. In the command line, run: `python main.py`. The first time you run the program, you will be prompted to create a binary file with the vectors, forquicker future access. After that, you can enter the desired word and get its closest homophones.

--lenakmeth

# When starting the program you may choose between the different vector models which are in text format out of the box.
# As the loading of binary files is a lot faster, the program will prefer them over .txt files in case of there being a file with the same name, but .bin ending.
# You will be offered to create a binary file corresponding to the .txt file you put in, unless there already is one.


eazteregg
