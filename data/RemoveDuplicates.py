# -*- coding: utf-8 -*-
"""
Created on Thu Jun 22 14:50:40 2017

@author: Max
"""
import os

# Get file paths to corpus.
script_path = os.path.abspath(__file__) # i.e. /path/to/dir/RemoveDuplicates.py
script_dir = os.path.split(script_path)[0] #i.e. /path/to/dir/
rel_path = "idiom_corpus.txt"
abs_file_path_corpus = os.path.join(script_dir, rel_path)

corpus = dict()
is_idiom = True
key = "" #idioms
value = "" #explanations
with open(abs_file_path_corpus, 'r', encoding="utf-8") as f:
    for line in f:
        line = line.strip().lower()
        if (line.startswith('#')): continue
        if is_idiom:
            key = line.splitlines()[0]
            is_idiom = False
        else:
            value = line.splitlines()[0]
            corpus[key] = value
            is_idiom = True

print("original lines: 768")
print("lines after removing identical idioms and their explanations: {}".format(len(corpus)*2))            

# Some idioms might differ slightly because one version starts with a determiner while another version doesn't.
# Remove all similar idioms if they are the same after the first word.
keys = list(corpus.keys())
short_keys = list()
#for key in corpus.keys(): # This does not work because the dictionary changes size during iteration.
for key in keys:
    # Remove idioms that consist of only 1 word. 
    # E.g. "scapegoat", "doozy", "jaywalk", "southpaw"
    if (not len(key.split(' ')) > 1):
        del corpus[key]
    else:
        # Compare starting from the second word.
        short_keys += [key.split(' ',1)[1]] #['word1', 'word2 word3 word...']
'''
print(len(short_keys))
s = list(set(short_keys))
print(len(s))
duplicates = set([x for x in short_keys if short_keys.count(x) > 1])
print(duplicates)
# All false alarms, like slow down, calm down, get down, old horse, dark horse...
'''
print("lines after deleting one-word-idioms: {}".format(len(corpus)*2))

#TODO: Write corpus to file
with open("corpus_clean.txt", 'w', encoding="utf-8") as f:
    f.write("# The first line is always an idiom, the following line is its explanation...")
    for i, e in corpus.items():
        f.write(i + '\n')
        f.write(e + '\n')
        
test = []
test2 = [1,2]

if test:
    print("test")
    
if len(test2)>1:
    print("test2")