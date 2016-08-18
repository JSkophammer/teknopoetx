import json
from techno_poet import *
from time import ctime
from text_format import update_main_vocab
from nltk.corpus import brown
from nltk.corpus import cmudict
import re
import nltk

entries = cmudict.entries()
prondict = cmudict.dict()

file1 = 'json/main_gram_dict.json'
file2 = 'json/main_rev_gram.json'
file3 = 'json/main_vocab.json'
file4 = 'json/pron_dict_main.json'

with open(file1) as f_obj1:
    main_gram_dict = json.load(f_obj1)

with open(file2) as f_obj2:
    main_rev_gram = json.load(f_obj2)

with open(file3) as f_obj3:
    main_vocab = json.load(f_obj3)

with open(file4) as f_obj4:
    pron_dict_main = json.load(f_obj4)

def update_main_gram_dict(vocab):
    print('Start:', ctime())
    new_voc = [w.lower() for w in vocab if w not in main_gram_dict.keys()]
    print(len(new_voc))
    gram_struc(new_voc)
    print('End:', ctime())


with open('json/vocab/ed_vocab.json') as f_obj_ed:
    ed_vocab = json.load(f_obj_ed)

with open('json/vocab/hp_vocab.json') as f_obj_hp:
    hp_vocab = json.load(f_obj_hp)

with open('json/vocab/poet_vocab.json') as f_obj_po:
    poet_vocab = json.load(f_obj_po)

with open('json/vocab/js_vocab.json') as f_objpt:
    js_vocab = json.load(f_objpt)

with open('json/vocab/pd_vocab.json') as f_objpd:
    pd_vocab = json.load(f_objpd)

with open('/users/jason/python/texts/poems.txt') as f_obj0:
    poems = f_obj0.read()

poem_words = nltk.wordpunct_tokenize(poems.lower())

roman = [w for w in poem_words if re.findall(r'^[ivxlc]+$', w)]
roman.remove('i')

for x in roman:
    if x in poem_words:
        poem_words.remove(x)

clean = ' '.join(poem_words)
with open('/users/jason/python/texts/poems.txt', 'w') as f_obj:
    poems = f_obj.write(clean)

"""

update_main_gram_dict(pd_vocab)

with open('json/vocab/js_vocab.json', 'w') as f_obj_ed3:
    json.dump(js_vocab, f_obj_ed3)



with open('json/vocab/ed_vocab.json') as f_obj_ed3:
    ed_vocab_new = json.load(f_obj_ed3)

print(len(ed_vocab_new))

print(len(poet_vocab))

poetry_vocab = list(set(js_vocab + poet_vocab))

pron_vocab = [w for w in pron_dict_main.keys()]
for w in pron_vocab:
    if w not in main_vocab:
        main_vocab.append(w)


with open(file3, 'w') as f_obj:
    json.dump(main_vocab, f_obj)


#new_vocab = [w.lower() for w in main_vocab if w not in pron_dict_main.keys()]
#print(len(new_vocab))


b_gram_dict = {k: v for k, v in brown.tagged_words()}
print(len(b_gram_dict))

for k, v in b_gram_dict.items():
    main_gram_dict[k] = v

with open(file1, 'w') as f_obj:
    json.dump(main_gram_dict, f_obj)

main_gram_vocab = [w.lower() for w in main_gram_dict.keys()]
print(len(main_gram_vocab))

b_rev_dict = {v: [k for k in b_gram_dict.keys() if b_gram_dict[k] == v] for k, v in b_gram_dict.items()}


with open(file2, 'w') as f_obj:
    json.dump(b_rev_dict, f_obj)

out = ['oyt','sa','nay','ry','ha','da','ooh','ful','um','mm','ter','fro','ley','fé','yer','liv','nof', 'eh','roe','re',
       'ube', 'aha','un','hmm','upf','lo', 'sp', 'erm', 'en','doi', 'th','teh','yeh','er', 'las','ah','fer','isn','oh',
       'jus','sc','mon','mr', 'nah','li','gar', 'id','oy','sn','ye', 'jew', 'aff','sex','ne','ing','o', 'chf','st','mar',
       'ref', 'em','de', 'ho','sec','sud','gay','ere', 'don','hie']
out2 = ['asks', 'wasn','fête','asks','shoo','kidd',
'thro',
'wham',
'etna',
'yeah', 'aaah',
'ehru',
'hadn',
'hasn',
'otis',
'bott',
'peru',
'mong',
'tyke',
'stra',
'newt',
'itoo',
'todd',
'abou',
'nmat',
'sorc',
'mien',
'dium',
'urgh',
'atta',
'ebbs', 'hehe',
'diff',
'goin',
'hmmm']
"""