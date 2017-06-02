#!/usr/bin/env python3

import argparse
from SearchEngine import SearchEngine

if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description='Helps you build puns and lyrics')
    parser.add_argument('--vecs', type=str, default="glove.6B.100d.txt", help="Path to Glove/word2vec file (default: %(default)s)")
    parser.add_argument('--combo', type=str, default="sum", help="Combination method {sum|prod|inter} (default: %(default)s)")
    parser.add_argument('--rhyme', action="store_true", help="Restrict phonological matches to rhymes")
    parser.add_argument('--ortho', action="store_true", help="Use orthographic matches instead of phonological ones")
    cmd_args = parser.parse_args()

    print("Hello and welcome to the pun aid!")
    se = SearchEngine(1000, cmd_args.vecs, combine='s')
    se.combine = cmd_args.combo

    while True:

        query = input("Start search: \"Sounds like x\" \"Has to do with y\":\n> ")
        query = query.split()

        if not query:
            break

        elif len(query) > 2:
            print("Sorry, you need to provide two arguments!")
            continue
        else:
            print(se.execute_query(query[0], query[1]))
