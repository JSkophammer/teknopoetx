'''
import json
from nltk.corpus import stopwords
from settings import Settings
'''
import pandas as pd
#from txt_admin import update_all
'''
mset = Settings()
stop_words = stopwords.words('english')
word_freq = json.load(open('nov_fdist.json'))

tot_words = [word for word, freq in word_freq if (freq > 0 and mset.syl_count[word] != 0)
             and freq != mset.syl_count[word]]

stp_words = [w for w in stop_words if w in tot_words]

trn_words = tot_words[:14000]
tst_words = tot_words[14000:]

fdist_dct = {word: freq for word, freq in word_freq}

test_dict = {}
for word in trn_words:
    if (fdist_dct[word]/mset.syl_count[word]) < 1:
        test_dict[word] = 1
    else:
        test_dict[word] = -1


word_data = []
for i in range(len(trn_words)):
    word = trn_words[i]
    word_data.append([word, 1/fdist_dct[word], 1/mset.syl_count[word], test_dict[word]])

df = pd.DataFrame(word_data)

df.columns = ['word', 'freq', 'numsyl', 'stop']

df.to_csv('csv/trn_data.csv', header=None)
'''
df2 = pd.read_csv('csv/seizure.csv')

print(df2.tail)


'''






#df2_index = df2['words']
#print(type(df2_index[:10].values.tolist()))
#print(df2['strs pat'].loc['fragment'])

def dfind(dataframe, word):
    d_find = dataframe['words'].values.tolist().index(word)
    return d_find

print(dfind(df2, 'cat'))
'''