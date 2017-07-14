#!/usr/bin/env python3
import sys
import argparse
from FindRelatedSentences import FindRelatedSentences
from WordInsert import WordInsert
from SearchEngine import SearchEngine

if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description='Helps you build puns and lyrics')
    parser.add_argument('--vecs', type=str, default="glove.6B.50d.txt", help="Path to Glove/word2vec file (default: %(default)s)")
    parser.add_argument('--combo', type=str, default="sum", help="Combination method {sum|prod|inter} (default: %(default)s)")
    parser.add_argument('--rhyme', action="store_true", help="Restrict phonological matches to rhymes")
    parser.add_argument('--ortho', action="store_true", help="Use orthographic matches instead of phonological ones")
    parser.add_argument('--buckeye', action="store_true", help="Use Buckeye Prononciation Dictionary")
    parser.add_argument('--expl', action="store_true", help="Also use explanations of idioms")
    parser.add_argument('--sound_like', type=str, help="Specify 'sounds-like' word")
    parser.add_argument('--means', type=str, help="Specify 'meaning' word")
    parser.add_argument('--verbose', action="store_true", help="Print additional debugging info")
    parser.add_argument('--func', action="store_true", help="Consider function words for replacement.")
    parser.add_argument('--joke', action="store_true", help="Results are jokes.")
    cmd_args = parser.parse_args()

    print("Hello and welcome to the pun aid!")
    se = SearchEngine(1000, cmd_args.vecs, cmd_args.combo)
    model = se.word_vectors

    if cmd_args.ortho and cmd_args.rhyme:
        print('Looking for both orthographic matches and rhyming matches is not possible. Please choose one!')
        sys.exit()

    while True:

        query = input("Start search: \"Sounds like x\" \"Has to do with y\":\n> ")
        query = query.split()

        if not query:
            print("Bye, byeee!! Sorry, no pun available for this prompt, yet...")
            break

        elif len(query) != 2:
            print("Sorry, you need to provide two arguments!")
            continue
        else:


            sounds_like = query[0]
            topic = query[1]
            print(se.execute_query(sounds_like, topic, cmd_args.ortho, cmd_args.buckeye, cmd_args.rhyme, cmd_args.verbose))
            print("Puns: (•_•)  ( •_•)>⌐■-■  (⌐■_■)")

            frs = FindRelatedSentences(topic, model, cmd_args.verbose, max_results=300, expl=cmd_args.expl)
            new_corpus = frs.filter_sentences_by_topic()
            wi = WordInsert(se.best_result, new_corpus, True, max_distance=1, joke=cmd_args.joke)
            for s in wi.insert_word():
                print(s)
