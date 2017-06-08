# Pun-Intended
An application designed to help users find puns.

Notes on how to get the program to work:

Now needs nltk with cmudict!

1.
Get gensim running which requires some workarounds on windows as you'll be needing numpy+mkl and scipy which can be found
on http://www.lfd.uci.edu/~gohlke/pythonlibs/

2.
Now, what I did was download the gloVe 6B Vectors based on the Wikipedia2014 and Gigaword5 corpus. https://nlp.stanford.edu/projects/glove/
Add them to the data folder.

When starting the program you may choose between the different vector models which are in text format out of the box.
As the loading of binary files is a lot faster, the program will prefer them over .txt files in case of there being a file with the same name, but .bin ending.
You will be offered to create a binary file corresponding to the .txt file you put in, unless there already is one.


eazteregg
