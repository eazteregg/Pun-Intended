from nltk.corpus import cmudict
import json, re

file = open('./data/buckeye_pronunciation_dictionary.json', encoding = 'utf-8').read()
buck = json.loads(file)
cmu = cmudict.dict()


for i in buck[1]:
    if i in cmu:
        cmu_tr = re.sub('[0-9]', '', ' '.join(cmu[i][0]).lower())
        bu_tr = buck[1][i]
        if cmu_tr in bu_tr:
            print('ok')
        else:
            print(cmu_tr, bu_tr)
        
