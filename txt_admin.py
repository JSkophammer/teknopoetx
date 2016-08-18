from teknopoetx import *
from txt_formt import *
import json

mn_vocb = '/users/jason/teknopoetx/j_son/main_vocb.json'
syl_cnt = '/users/jason/teknopoetx/j_son/syl_count.json'
rv_gram = '/users/jason/teknopoetx/j_son/mrev_gram.json'
mn_gram = '/users/jason/teknopoetx/j_son/main_gram.json'
str_dct = '/users/jason/teknopoetx/j_son/strs_dict.json'
prn_dct = '/users/jason/teknopoetx/j_son/pron_dict.json'

anlz = Anlyz()
sett = Settings()


def word_list(textfile):
    file = open(textfile)
    text_string = file.read()
    all_words = wordpunct_tokenize(text_string)
    return all_words


def gen_text_log(sent, sent_source):
    fname = 'logs/js_poems/log-' + sent_source
    file = open(fname, 'a')
    file.write(sent + '\n')
    file.close()


def gen_words(vocab, group_id):
    word_dict = {}
    for word in vocab:
        word_dict[word] = Word(word)
    f_id = 'j_son/' + group_id + 'w_dict.json'
    json.dump(word_dict, open(f_id, 'w'))


def gen_gram_strc():
    gen_frms = json.load(open('j_son/gram_strc/pdl_sentlines.json'))
    grm_lins = json.load(open('j_son/gram_strc/pdl_gramlines.json'))
    gram_strc = {}
    for i in range(len(gen_frms)):
        gram_strc[int(i)] = (gen_frms[i], grm_lins[i])
        print(grm_lins[i])
    json.dump(gram_strc, open('j_son/gram_strc/' + sett.file_idn + '_grmstrc.json', 'w'))
    return gram_strc


def gen_main_dict(vocab, file_id=''):
    txt_dict = {}
    for word in vocab:
        txt_dict[word] = dict(pos=sett.main_gram[word.lower()], strs=sett.strs_dict[word.lower()],
                              pron=sett.pron_dict[word.lower()], numsyl=sett.syl_count[word.lower()])
    filename = '/users/jason/teknopoetx/j_son/' + file_id + 'txt_dict.json'
    with open(filename, 'w') as maind: json.dump(txt_dict, maind)


def gen_freq_pron():
    cmu_pdict = sett.cmu_pdict
    pron_vocab = [w.lower() for w in cmu_pdict.keys()]
    cmu_phon_clus = [(w, anlz.phon_clus(w), cmu_pdict[w][0]) for w in pron_vocab]
    cm_pc_std = [(x, y, z) for x, y, z in cmu_phon_clus if len(y) == len(z)]
    cm_fin = [(x, y, z) for x, y, z in cm_pc_std if anlz.sim_phon(y, z)]
    clus_list = [cm_fin[i][1] for i in range(len(cm_fin))]
    clus_fn = []
    for l in clus_list:
        for clus in l:
            clus_fn.append(clus)
    clus_fin = list(set(clus_fn))
    high_freq = {}
    for clus in clus_fin:
        high_freq.setdefault(clus, [])
    for x, y, z in cm_fin:
        for i in range(len(y)):
            high_freq[y[i]].append(z[i])
    keys = list(high_freq.keys())
    for k in keys:
        if not k.isalpha():
            high_freq.pop(k)
    with open('j_son/pron_freq2.json', 'w') as f_objpf:
        json.dump(high_freq, f_objpf)
    freq_pron = {}
    for clus in high_freq.keys():
        freq_pron.setdefault(clus, [])
    for key, value in high_freq.items():
        val = list(set(value))
        for phon in val:
            phon_perc = value.count(phon) / len(value)
            if phon_perc > .15:
                freq_pron[key].append(phon)
    json.dump(freq_pron, open('j_son/freq_pron.json', 'w'))
    return freq_pron


def combine_dict(dict1, dict2, f_id):
    combine_d = {}
    comb_dict = {}
    comb_keys = list(set(list(dict1.keys()) + list(dict2.keys())))
    for key in comb_keys:
        comb_dict.setdefault(key, [])
    for key1 in dict1.keys():
        comb_dict[key1] += dict1[key1]
    for key2 in dict2.keys():
        comb_dict[key2] += dict2[key2]
    for key in comb_keys:
        combine_d[key] = list(set(comb_dict[key]))
    file_id = 'j_son/rev_gram/' + f_id + '_combd.json'
    with open(file_id, 'w') as f_objid:
        json.dump(combine_d, f_objid)
    return combine_d


def fix_strs_dict(vocab, strs_dict=sett.strs_dict):
    strs_pat = ''
    for word in vocab:
        if word in sett.cmu_pdict.keys():
            strs_pat = strs_dict[word]
            strs_pat = strs_pat.replace('2', '1')
            strs_dict[word] = strs_pat
    fix_strs = [w for w in vocab if w not in sett.cmu_pdict.keys() and strs_dict[w]]
    for wrd in fix_strs:
        if wrd in strs_dict.keys():
            strs_pat = strs_dict[wrd]
        else:
            pron = anlz.gen_pron(wrd)
            for i in range(len(pron)):
                if pron[i][-1].isdigit():
                    strs_pat += pron[i][-1]
        strs_pat = strs_pat.replace('2', '1')
        if strs_pat[0] == '0':
            for i in range(len(strs_pat)):
                strsl = list(strs_pat)
                strsl[i] = str(i % 2)
                strs_pat = ''.join(strsl)
        else:
            for i in range(len(strs_pat)):
                strsl = list(strs_pat)
                strsl[i] = str((i + 1) % 2)
                strs_pat = ''.join(strsl)
        strs_dict[wrd] = strs_pat

    with open(str_dct, 'w') as fob5:
        json.dump(strs_dict, fob5)

