#!/usr/bin/env python3

from SearchEngine import SearchEngine
import sys
if __name__ == "__main__":

    if len(sys.argv) < 2:
        print("Please specify the word2vec or gloVe vector file as 2nd argument.")
        sys.exit()

    print("Hello and welcome to the pun aid!")
    se = SearchEngine(1000, sys.argv[1], combine='s')

    while True:

        query = input("\"Sounds like x\" \"Has to do with y\"")
        query = query.split()

        if not query:
            break

        elif len(query) > 2:
            print("Sorry, you need to provide two arguments!")
            continue
        elif len(query) == 1:
            if query[0] == '-s':
                se.combine = 's'
            elif query[0] == '-p':
                se.combine = 'p'
            elif query[0] == '-i':
                se.combine = ''
            else:
                print('To change combination method please use: -i -p -s ')
                continue
        else:

            print(se.execute_query(query[0], query[1]))