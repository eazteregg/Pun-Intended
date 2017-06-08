# Pun-Intended
An application designed to help users find puns.

Notes on how to get the program to work:

1.
Get gensim running which requires some workarounds on windows as you'll be needing numpy+mkl and scipy which can be found
on http://www.lfd.uci.edu/~gohlke/pythonlibs/

2.
Now, what I did was download the gloVe 6B Vectors based on the Wikipedia2014 and Gigaword5 corpus. https://nlp.stanford.edu/projects/glove/
Add them to the data folder.

When starting the program you may choose between the different vector models which are in text format out of the box.
As the loading of binary files is a lot faster, the program will prefer them over .txt files in case of there being a file with the same name, but .bin ending.
You will be offered to create a binary file corresponding to the .txt file you put in, unless there already is one.

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


eazteregg
