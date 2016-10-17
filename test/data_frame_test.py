import pandas as pd
#from techno_poet import *
import json

with open('json/main_vocab.json') as f_obj0:
    m_voc = json.load(f_obj0)
with open('json/vocab/poet_vocab.json') as f_obj1:
    poet_vocab = json.load(f_obj1)
with open('json/pron_dict_main.json') as f_obj2:
    p_d_m = json.load(f_obj2)
with open('json/strs_dict.json') as f_obj3:
    s_d = json.load(f_obj3)
with open('json/syl_cnt_d.json') as f_obj4:
    syl_d = json.load(f_obj4)
with open('json/main_gram_dict.json') as f_obj5:
    m_g_d = json.load(f_obj5)
with open('json/vocab/js_vocab.json') as f_obj6:
    js_voc = json.load(f_obj6)

with open('json/vocab/js_sort_voc.json') as f_obj7:
    js = json.load(f_obj7)

main = sorted([w for w in m_voc if w in p_d_m.keys() and w in s_d.keys()
               and w in syl_d.keys() and w in m_g_d.keys() and w.isalpha()])


with open('json/vocab/m_voc.json', 'w') as fmv:
    json.dump(main, fmv)

'''
print(len(main))
word_data = []

for i in range(len(main)):
    word_data.append([main[i], p_d_m[main[i]], s_d[main[i]], syl_d[main[i]], m_g_d[main[i]]])


df = pd.DataFrame(word_data)

df.columns = ['words', 'pron', 'strs', 'numsyl', 'pos']

df.to_csv('csv/main_vocdf.csv', sep='\t')



df2 = pd.read_csv('js_vocab_df.csv', sep='\t')

#df2_index = df2['words']
#print(type(df2_index[:10].values.tolist()))
#print(df2['strs pat'].loc['fragment'])

def dfind(dataframe, word):
    d_find = dataframe['words'].values.tolist().index(word)
    return d_find

print(dfind(df2, 'cat'))



def same_syls(word1, word2):
    if df2['numsyl'].iloc[js.index(word1)] == df2['numsyl'].iloc[js.index(word2)]:
        return True
    else:
        return False

print(same_syls('up', 'down'))
print(same_syls('forget', 'it'))

#print(df2['pos_tag'].iloc[js.index('king')])



with open('json/vocab/js_sort_voc.json', 'w') as fobj1:
    json.dump(main, fobj1)


df = pd.DataFrame([['cat', phon_clus('cat'), pron_dict_main['cat'], count_syl('cat'), strs_pattrn('cat')],
                  ['rabbit', phon_clus('rabbit'), pron_dict_main['rabbit'],count_syl('rabbit'), strs_pattrn('rabbit')],
                  ['real', phon_clus('real'), pron_dict_main['real'], count_syl('real'), strs_pattrn('real')]])
df.columns = ['word', 'phonetic clusters', 'pronunciation', '# of syls', 'strs pattern']
print(df)

categories = ['word', 'phonetic clusters', 'pronunciation', '# of syls', 'strs pattern', 'pos tag', 'rhyme syl',
              'vowel index', 'consonant index', 'pronun vowel index', 'pronun consonant index', 'vowel cluster index',
              'vowel clusters', 'consonant clusters']
# potential categories = 'synonyms', 'most frequent bigrams', 'antonyms'
'''
