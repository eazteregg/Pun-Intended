import json
from nltk.metrics import *



def readDictJson(path_to_file):
    dict_in_json = open(path_to_file, encoding='utf-8').read()
    return json.loads(dict_in_json)


def findSimilarWords(word, word_tr_dict, tr_word_dict):
    similar_wordsVSdist = {}
    given_tr = word_tr_dict[word]
    for transcrip in given_tr:
        for i in tr_word_dict:
            dist = edit_distance(transcrip.split(), i.split()) 
            if dist <= len(word)/2 and dist != 0:
                for transcr in tr_word_dict[i]:
                    similar_wordsVSdist[transcr] = dist
    return similar_wordsVSdist


def similarFromBuckeye(word, path_to_file):
    tr_word, word_tr = readDictJson(path_to_file)
    list_of_words_dist = findSimilarWords(word, word_tr, tr_word)
    return list_of_words_dist

if __name__ == "__main__":
    l = similarFromBuckeye('dog', './data/buckeye_pronunciation_dictionary.json')
    for i in l:
        print(i, l[i])
