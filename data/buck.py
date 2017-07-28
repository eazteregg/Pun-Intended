import json
f = open('buckeye_pronunciation_dictionary.txt', encoding='utf-8')
d = {}      # Dictionary: key - SAMPA, value - set of words
rev = {}    # Dictionary: key - word, value - set of possible transcriptions

counter = 0
for i in f:
    counter += 1
    print(round((counter/38520) * 100), '%', end="\r")
    sampa = ' '.join(i.split()[1:-2])
    word = i.split()[0]
    sampa = ' '.join(i.split()[1:-2])
    if sampa not in d:
        d[sampa] = [word]
    else:
        d[sampa].append(word)
    if word not in rev:
        rev[word] = [sampa]
    else:
        rev[word].append(sampa)
        
print('Buckeye Pronunciation Dictionary is ready')
print('Name of file is "buckeye_pronunciation_dictionary.json"')

dj = json.dumps([d, rev])
buck = open('buckeye_pronunciation_dictionary.json', 'w', encoding='utf-8')
buck.write(dj)
buck.close()


