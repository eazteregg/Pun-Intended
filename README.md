# Pun-Intended
An application designed to help users find puns.

Note on how to get the program to work:

Unfortunately, github won't let me push the word vector file to the remote repository as it takes up too much space I guess which
is why I'm posting this here.

1.
Get gensim running which requires some workarounds on windows as you'll be needing numpy+mkl and scipy which can be found
on http://www.lfd.uci.edu/~gohlke/pythonlibs/

2.
Now, what I did was download the gloVe 6B Vectors based on the Wikipedia2014 and Gigaword5 corpus. https://nlp.stanford.edu/projects/glove/

Then I used gensim to transform the gloVe format into the word2vec format (gensim requires word2vec I believe), the only difference between the two being
an additional line at the top of the file which holds information about the number of vectors and their dimensionality.

eazteregg
