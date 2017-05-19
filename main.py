#!/usr/bin/env python3

from SearchEngine import SearchEngine

if __name__ == "__main__":

    print("Hello and welcome to the pun aid!")
    se = SearchEngine(1000)

    while True:

        query = input("\"Sounds like x\" \"Has to do with y\"")
        query = query.split()

        if not query:
            break
        elif len(query) != 2:
            print("Sorry, you need to provide two arguments!")
            continue

        print(se.execute_query(query[0], query[1]))