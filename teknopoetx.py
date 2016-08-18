from random import choice
from nltk import pos_tag
import txt_admin as admin
from txt_formt import remove_punct
from txt_formt import lower_case
from settings import Settings
import re
import json
import abc


# Contains a variety of functions used to analyze texts
class Anlyz:
    def __init__(self):
        self.sett = Settings()
        self.vows = ['A', 'E', 'I', 'O', 'U', 'Y', 'a', 'e', 'i', 'o', 'u', 'y']
        self.cnst = 'bcdfghjklmnpqrstvwxzBCDFGHJKLMNPQRSTVWXZ'
        self.cnsl = 'bcdfghjklmnpqrstvwxz'
        self.cnsu = 'BCDFGHJKLMNPQRSTVWXZ'
        self.prnv = ['A', 'E', 'I', 'O', 'U']
        self.prnc = list(self.cnsu)
        self.cncl = ['sh', 'ch', 'th', 'ph', 'ng']

    # Determines total time elapsed during program execution
    @staticmethod
    def time_elapse(start, end):
        t1 = start.split()[3].split(':')
        t2 = end.split()[3].split(':')
        hours = int(t2[0]) - int(t1[0])
        minutes = int(t2[1]) - int(t1[1])
        seconds = int(t2[2]) - int(t1[2])
        if seconds < 0:
            seconds += 60
            minutes -= 1
        if minutes < 0:
            minutes += 60
            hours -= 1
        if hours < 10:
            hours = '0' + str(hours)
        else:
            hours = str(hours)
        if minutes < 10:
            minutes = '0' + str(minutes)
        else:
            minutes = str(minutes)
        if seconds < 10:
            seconds = '0' + str(seconds)
        else:
            seconds = str(seconds)
        print('\nTotal time = ' + hours + ':' + minutes + ':' + seconds + '\n')

    # Returns elements common to list1 and list2
    @staticmethod
    def list_inter(list1, list2):
        in_both = []
        for elem in list1:
            if elem in list2:
                in_both.append(elem)
        return in_both

    # Determines the index of phonetic clusters for a given word
    @staticmethod
    def clusters(let_list):
        count = 0
        end = []
        while count < len(let_list):
            p = [let_list[count]]
            while (count < (len(let_list) - 1)) and let_list[count] + 1 == let_list[count + 1]:
                p.append(let_list[count + 1])
                if count == len(let_list) - 1:
                    break
                else:
                    count += 1
            count += 1
            end.append(p)
        return end

    # Determines indices of all vowels in a word
    def vowel_index(self, word):
        vow_ind = []
        for i in range(len(word)):
            if word[i] in self.vows:
                vow_ind.append(i)
        return vow_ind

    # Determines indices of all consonants in a word
    def cons_index(self, word):
        cons_ind = []
        for i in range(len(word)):
            if word[i] not in self.vows:
                cons_ind.append(i)
        return cons_ind

    # Determines indices for vowel phonemes in a word
    def pron_v_ind(self, word):
        pron_dict = self.sett.pron_dict
        pron = pron_dict[word]
        pron_vow_ind = []
        for i in range(len(pron)):
            if pron[i][0] in self.prnv:
                pron_vow_ind.append(i)
        return pron_vow_ind

    # Determines indices for consonant phonemes in a word
    def pron_c_ind(self, word):
        pron = self.sett.pron_dict[word]
        pron_con_ind = []
        for i in range(len(pron[0])):
            if pron[0][i][0] in self.prnc:
                pron_con_ind.append(i)
        return pron_con_ind

    # Determines indices for vowel clusters in a word
    def clus_v_ind(self, word):
        phon = self.phon_clus(word)
        phon_clus_ind = []
        for i in range(len(phon)):
            if phon[i][0] in self.vows:
                phon_clus_ind.append(i)
        return phon_clus_ind

    # Generates list of vowel clusters in a word
    def v_clus(self, word):
        v_ind = self.vowel_index(word)
        v_ind_clus = self.clusters(v_ind)
        v_clusters = []
        for v in v_ind_clus:
            first = v[0]
            length = len(v)
            seg = word[first: first + length]
            v_clusters.append(seg)
        return v_clusters

    # Generates list of consonant clusters in a word
    def c_clus(self, word):
        c_ind = self.cons_index(word)
        c_ind_clus = self.clusters(c_ind)
        c_clusters = []
        for c in c_ind_clus:
            first = c[0]
            length = len(c)
            seg = word[first: first + length]
            c_clusters.append(seg)
        return c_clusters

    # Generates a list of all phonetic clusters in a word
    def phon_clus(self, word):
        phones = []
        v_cl = self.v_clus(word)
        c_cl = self.c_clus(word)
        if 0 in self.cons_index(word):
            phon_cl = c_cl[:]
            for n in range(len(v_cl)):
                phon_cl.insert(1 + (2 * n), v_cl[n])
        else:
            phon_cl = v_cl[:]
            for n in range(len(c_cl)):
                phon_cl.insert(1 + (2 * n), c_cl[n])
        for cl in phon_cl:
            if (cl[0] in self.cnst) and (cl not in self.cncl) \
                    and (len(set(list(cl))) > 1):
                phones += list(cl)
            else:
                phones.append(cl)
        if phones[-1] == 'e' or phones[-1] == 'E':
            phones.pop()
        return phones

    # Determines if phonetic clusters sound the same
    def sim_phon(self, phon_cls, word_phon):
        sim = True
        for i in range(len(word_phon)):
            if word_phon[i] in self.cnsu:
                if word_phon[i] == 'K' and phon_cls[i] == 'c':
                    sim = True
                elif word_phon[i].lower() != phon_cls[i]:
                    sim = False
        return sim

    # Determines the most frequent sound associated with a given phonetic cluster
    def most_freq(self, clus):
        phon = self.sett.freq_pron[clus]
        freq = list(set([p for p in phon if phon.count(p) == max([phon.count(c) for c in list(set(phon))])]))
        return freq

    # Determines the last vowel in a word
    def last_vowel(self, word):
        pron_dict = self.sett.pron_dict
        last_vows = []
        if word.lower() in list(pron_dict.keys()):
            pron = pron_dict[word.lower()]
        else:
            pron = self.gen_pron(word.lower())
        index = -1
        while -len(pron) <= index < 0:
            if pron[index][0] in self.vows:
                last_vows.append(pron[index])
                index = 0
            else:
                index -= 1
        return last_vows

    # Determines the last syllable in a word
    def last_syl(self, word):
        pron_dict = self.sett.pron_dict
        last_syls = []
        if word.isalpha():
            if word in pron_dict.keys():
                pron = pron_dict[word]
            else:
                pron = self.gen_pron([word])
            index = -1
            while -len(pron) <= index < 0:
                if pron[index][0] in self.vows:
                    vow = pron[index][:2]
                    pron[index] = vow
                    last_syls = pron[index:]
                    index = 0
                else:
                    index -= 1
        return last_syls

    # Determines whether or not word1 rhymes with word2
    def rhyme_test(self, word1, word2):
        try:
            if self.list_inter(self.last_syl(word1), self.last_syl(word2)):
                return True
            else:
                return False
        except:
            return False

    # Determines the stress (or accent) pattern in a word
    def strs_pattrn(self, word):
        pron_dict = self.sett.pron_dict
        strs_dict = self.sett.strs_dict
        strs_pat = ''
        if word.isalpha():
            if word in pron_dict.keys():
                pron = pron_dict[word]
            else:
                print('gen_pron:', word)
                pron = self.gen_pron(word)
            for i in range(len(pron)):
                if pron[i][-1].isdigit():
                    strs_pat += pron[i][-1]
            strs_pat = strs_pat.split()
            strs_pat = ''.join(strs_pat)
            strs_dict[word] = strs_pat
        return strs_pat

    # Determines the number of syllables in a word
    def count_syl(self, word):
        strs_dict = self.sett.strs_dict
        num_syls = 0
        if word.isalpha():
            if word in strs_dict.keys():
                num_syls = len(strs_dict[word])
            else:
                num_syls = len(self.strs_pattrn(word))
        return num_syls

    # Generates the most probable pronunciation for a word
    def gen_pron(self, word):
        prondict = self.sett.cmu_pdict
        pron_dict = self.sett.pron_dict
        freq_pron = self.sett.freq_pron
        if word not in prondict.keys():
            word_pron = []
            phon_cl = self.phon_clus(word)
            for i in range(len(phon_cl)):
                if phon_cl[i].lower() in freq_pron.keys():
                    phon = choice(freq_pron[phon_cl[i].lower()])
                else:
                    phon = phon_cl[i].upper()
                word_pron.append(phon)
            pron_dict[word] = word_pron
        else:
            word_pron = prondict[word][0]
        return word_pron

    # Determines the parts of speech for all words in a list
    def gram_struc(self, wordlist):
        mrev_gram = self.sett.mrev_gram
        main_gram = self.sett.main_gram
        sent_pos = []
        for word in wordlist:
            if word in main_gram.keys():
                sent_pos.append(main_gram[word])
            else:
                pos = pos_tag([word])[0][1]
                sent_pos.append(pos)
                main_gram[word] = pos
                if pos in mrev_gram.keys():
                    mrev_gram[pos].append(word)
                else:
                    mrev_gram[pos] = [word]
        return sent_pos


class File:
    __metaclass__ = abc.ABCMeta

    def __init__(self, f_id='', add=None):
        self.sett = Settings()
        self.anlz = Anlyz()
        self.add = add
        self.fnct = (lambda x: x == x)
        self.updt = self.sett.main_gram
        self.fltr = self.updt.keys()
        self.name = 'File'
        self.m_id = self.sett.main_id
        self.f_id = 'j_son/' + f_id + '.json'
        self.f_ex = self.sett.file_pth + self.f_id

    def generate(self, data):
        gen = self.process(data)
        self.save_data(gen, self.f_ex)
        return gen

    def update(self):
        main_file = self.updt
        new = [w for w in self.add if w not in self.fltr]
        print(self.name + ': ' + str(len(new)) + 'words to update')
        self.enter(main_file, new)
        self.save_data(main_file, self.m_id)
        print(self.name, 'update complete\n')

    def process(self, data):
        words = list(set(remove_punct(data)))
        new_dict = {}
        self.enter(new_dict, words)
        return new_dict

    def enter(self, main_file, data):
        for x in data:
            if x in self.fltr and self.updt[x]:
                main_file[x] = self.updt[x]
            else:
                print(x)
                main_file[x] = self.fnct(x)

    @staticmethod
    def save_data(data, ext):
        json.dump(data, open(ext, 'w'))


class Vocab(File):
    def __init__(self, f_id='', add=None):
        super(Vocab, self).__init__(f_id='', add=None)
        self.add = add
        self.updt = self.sett.main_vocb
        self.fltr = self.sett.main_vocb
        self.name = 'Vocab'
        self.m_id = self.sett.vocb_id
        self.f_id = 'j_son/vocab/' + f_id + '_vocb.json'
        self.f_ex = self.sett.file_pth + self.f_id

    def process(self, file):
        words = admin.word_list(file)
        voc = list(set(remove_punct(words)))
        vocab = list(set([w for w in voc if w.isalpha()]))
        vocab += lower_case(vocab)
        vocab = list(set(vocab))
        for x in [w for w in vocab if re.findall(r'^[ivxlcIVXLC]+$', w)
        and w not in ['I', 'i', 'Ill', 'ill', 'civil', 'Civil']]:
            vocab.remove(x)
        return vocab

    def enter(self, main_file, word_list):
        for word in word_list:
            print(word)
            main_file.append(word)
        return main_file


class MainGram(File):
    def __init__(self, f_id='', add=None):
        super(MainGram, self).__init__(f_id='', add=None)
        self.add = add
        self.updt = self.sett.main_gram
        self.fltr = self.updt.keys()
        self.name = 'MainGram'
        self.m_id = self.sett.mgrm_id
        self.f_id = 'j_son/main_grm/' + f_id + '_mg.json'
        self.f_ex = self.sett.file_pth + self.f_id

    def enter(self, main_file, word_list):
        for word in word_list:
            if word in self.sett.brwn_dict.keys():
                pos = self.sett.brwn_dict[word]
            else:
                pos = pos_tag([word])[0][1]
            print(word)
            main_file[word] = pos
        return main_file


class RevGram(File):
    def __init__(self, f_id='', add=None):
        super(RevGram, self).__init__(f_id='', add=None)
        self.add = add
        self.updt = self.sett.mrev_gram
        self.fltr = self.sett.main_gram.keys()
        self.name = 'RevGram'
        self.m_id = self.sett.rgrm_id
        self.f_id = 'j_son/rev_gram/' + f_id + '_rg.json'
        self.f_ex = self.sett.file_pth + self.f_id

    def process(self, word_list):
        words = list(set(remove_punct(word_list)))
        old_words = [w for w in words if w in self.sett.main_gram.keys()]
        new_words = [w for w in words if w not in old_words]
        rev_gram = {}
        for pos in self.sett.main_gram.values():
            rev_gram.setdefault(pos, [])
        pairs = pos_tag(new_words)
        gram_list = list(set([y for x, y in pairs]))
        for pos in gram_list:
            rev_gram[pos] = list(set([pairs[i][0] for i in range(len(new_words)) if pairs[i][1] == pos]))
        for word in old_words:
            rev_gram[self.sett.main_gram[word]].append(word)
        return rev_gram

    def enter(self, main_file, word_list):
        for word in word_list:
            if word in self.sett.brwn_dict.keys():
                pos = self.sett.brwn_dict[word]
            else:
                pos = pos_tag([word])[0][1]
                print(word)
            if pos in main_file.keys():
                main_file[pos].append(word)
            else:
                main_file[pos] = [word]
        return main_file


class PronDict(File):
    def __init__(self, f_id='', add=None):
        super(PronDict, self).__init__(f_id='', add=None)
        self.add = add
        self.updt = self.sett.pron_dict
        self.fltr = self.updt.keys()
        self.fnct = (lambda x: self.anlz.gen_pron(x))
        self.name = 'PronDict'
        self.m_id = self.sett.pron_id
        self.f_id = 'j_son/pron_dct/' + f_id + '_prndct.json'
        self.f_ex = self.sett.file_pth + self.f_id


class StrsDict(File):
    def __init__(self, f_id='', add=None):
        super(StrsDict, self).__init__(f_id='', add=None)
        self.add = add
        self.updt = self.sett.strs_dict
        self.fltr = self.updt.keys()
        self.name = 'StrsDict'
        self.m_id = self.sett.strs_id
        self.f_id = 'j_son/strs_dct/' + f_id + '_strs.json'
        self.f_ex = self.sett.file_pth + self.f_id

    def enter(self, main_file, word_list):
        for word in word_list:
            print(word)
            main_file[word] = self.anlz.strs_pattrn(word)
        admin.fix_strs_dict(word_list, main_file)
        return main_file


class SylDict(File):
    def __init__(self, f_id='', add=None):
        super(SylDict, self).__init__(f_id='', add=None)
        self.add = add
        self.updt = self.sett.syl_count
        self.fltr = self.updt.keys()
        self.fnct = (lambda x: self.anlz.count_syl(x))
        self.name = 'SylDict'
        self.m_id = self.sett.sylc_id
        self.f_id = 'j_son/syl_cnt/' + f_id + '_sylc.json'
        self.f_ex = self.sett.file_pth + self.f_id


class RhymDict(File):
    def __init__(self, f_id='', add=None):
        super(RhymDict, self).__init__(f_id='', add=None)
        self.add = add
        self.updt = self.sett.rhym_dict
        self.fltr = self.updt.keys()
        self.fnct = (lambda x: self.anlz.last_syl(x))
        self.name = 'RhymDict'
        self.m_id = self.sett.rhym_id
        self.f_id = 'j_son/rhym_dct/' + f_id + '_rhym.json'
        self.f_ex = self.sett.file_pth + self.f_id


class S(str):
    def __init__(self, string):
        super(S, self).__init__()
        self.string = string
        self.list = list(self.string)
        self.len = len(self)

    def __and__(self, other):
        slice1 = [self.string[i:j] for i in range(len(self.string))
                  for j in range(1, len(self.string) + 1) if i < j]
        slice2 = [other.string[i:j] for i in range(len(other.string))
                  for j in range(1, len(other.string) + 1) if i < j]
        slice_inter = list(set([s for s in slice1 if s in slice2]))
        max_slice = [s for s in slice_inter if len(s) == max([len(s) for s in slice_inter])]
        return max_slice

    def __lt__(self, other):
        if isinstance(other, str):
            return self.string in other and self.string != other
        elif isinstance(other, S):
            return self.string in other.string and self.string != other.string

    def __gt__(self, other):
        if isinstance(other, str):
            return other in self.string and self.string != other
        elif isinstance(other, S):
            return other.string in self.string and other.string != self.string

    def __le__(self, other):
        if isinstance(other, str):
            return self.string in other
        elif isinstance(other, S):
            return self.string in other.string

    def __ge__(self, other):
        if isinstance(other, str):
            return other in self.string
        elif isinstance(other, S):
            return other.string in self.string

    def __iadd__(self, other):
        if isinstance(other, str):
            self.string += other
            return self
        elif isinstance(other, S):
            self.string += other.string
            return self

    def __sub__(self, other):
        if isinstance(other, str):
            return self.string.replace(other, '')
        elif isinstance(other, S):
            return self.string.replace(other.string, '')

    def __isub__(self, other):
        if isinstance(other, str):
            self.string -= other
            return self
        elif isinstance(other, S):
            self.string -= other.string
            return self

    def __mul__(self, other):
        if isinstance(other, str):
            return [self.string[i] + other[j] for i in range(len(self.string))
                    for j in range(len(other))]
        elif isinstance(other, S):
            return [self.string[i] + other.string[j] for i in range(len(self.string))
                    for j in range(len(other.string))]

    def __rmul__(self, other):
        if isinstance(other, str):
            return [other[j] + self.string[i] for i in range(len(self.string))
                    for j in range(len(other))]
        elif isinstance(other, S):
            return [other.string[j] + self.string[i] for i in range(len(self.string))
                    for j in range(len(other.string))]

    def __imul__(self, other):
        if isinstance(other, str):
            self = self.__mul__(other)
            return self
        elif isinstance(other, S):
            self = self.__mul__(other.string)
            return self

    def __pow__(self, power):
        mult = [self]
        for _ in range(power - 1):
            if len(mult) == 1:
                mult = self * self
            else:
                mult = [self.string[i] + s for i in range(len(self.string)) for s in mult]
        if power == 0:
            return [self.string]
        elif power == 1:
            return list(self.string)
        else:
            return mult


class Text:
    def __init__(self, filename, file_id):
        self.vocb = Vocab(file_id)
        self.rvgm = RevGram(file_id)
        self.mgrm = MainGram(file_id)
        self.strs = StrsDict(file_id)
        self.pron = PronDict(file_id)
        self.sylc = SylDict(file_id)
        self.rhym = RhymDict(file_id)
        self.filename = filename
        self.file_id = file_id
        self.file_ext = '/users/jason/teknopoetx/'

    @property
    def vocab(self):
        try:
            f_id = self.file_ext + 'j_son/vocab/' + self.file_id + '_vocab.json'
            with open(f_id) as file:
                text_voc = json.load(file)
            return text_voc
        except FileNotFoundError:
            Vocab(self.vocb.generate(self.filename)).update()
            MainGram(self.vocb.generate(self.filename)).update()
            RevGram(self.vocb.generate(self.filename)).update()
            StrsDict(self.vocb.generate(self.filename)).update()
            PronDict(self.vocb.generate(self.filename)).update()
            SylDict(self.vocb.generate(self.filename)).update()
            RhymDict(self.vocb.generate(self.filename)).update()

    @property
    def rev_gram(self):
        try:
            f_id = self.file_ext + 'j_son/rev_gram/' + self.file_id + '_rg.json'
            with open(f_id) as f_obj_rv:
                revgrm = json.load(f_obj_rv)
                return revgrm
        except FileNotFoundError:
            self.rvgm.generate(self.vocab)

    def formatted(self, filename, file_id, sett):
        from txt_formt import format_text
        format_text(self, filename, file_id, sett)


class Poem(Text):
    def __init__(self, filename, file_idn):
        super(Poem, self).__init__(filename, file_idn)
        self.anlz = Anlyz()
        self.sett = Settings()
        self.filename = filename
        self.file_idn = file_idn
        self.poem = open(filename).read()
        self.meter = self.get_meter()
        self.line_syl = self.get_line_syl()
        self.subject = self.get_subject()

    def get_meter(self):
        return self.poem

    def get_line_syl(self):
        line_syls = []
        for line in self.poem:
            syls = 0
            for word in line:
                syls += self.anlz.count_syl(word)
            line_syls.append(syls)
        return line_syls

    def get_subject(self):
        return self.poem


class Word(S):
    def __init__(self, word):
        super(S, self).__init__()
        self.word = word
        self.sett = Settings()
        self.anlz = Anlyz()

        # Associates word with part of speech, stress pattern, number of syllables, and phonetic description
        self.pstg = self.get_pstg()
        self.strs = self.get_strs()
        self.nsyl = self.get_nsyl()
        self.pron = self.get_pron()

    # Functions for generating above properties
    def genpron(self):
        return self.anlz.gen_pron([self.word])

    def strspattrn(self):
        return self.anlz.strs_pattrn(self.word)

    def countsyl(self):
        return self.anlz.count_syl(self.word)

    def get_pstg(self):
        try:
            return self.sett.main_gram[self.word]
        except:
            return self.anlz.gram_struc([self.word])[0]

    def get_pron(self):
        try:
            return self.sett.pron_dict[self.word]
        except:
            return self.anlz.gen_pron([self.word])[0]

    def get_strs(self):
        try:
            return self.sett.strs_dict[self.word]
        except:
            return self.anlz.strs_pattrn(self.word)

    def get_nsyl(self):
        try:
            return self.sett.syl_count[self.word]
        except:
            return self.anlz.count_syl(self.word)

    def __add__(self, other):
        return Word(self.word + other)

    # Breaks words into parts useful for determining the above properties
    def vin(self):
        return self.anlz.vowel_index(self.word)

    def cin(self):
        return self.anlz.cons_index(self.word)

    def pvin(self):
        return self.anlz.pron_v_ind(self.word)

    def vclin(self):
        return self.anlz.clus_v_ind(self.word)

    def vcls(self):
        return self.anlz.v_clus(self.word)

    def ccls(self):
        return self.anlz.c_clus(self.word)

    def phcls(self):
        return self.anlz.phon_clus(self.word)

    def lstv(self):
        return self.anlz.last_vowel(self.word)

    def lstsyl(self):
        return self.anlz.last_syl(self.word)


def update_all(vocab):
    Vocab(add=vocab).update()
    MainGram(add=vocab).update()
    RevGram(add=vocab).update()
    PronDict(add=vocab).update()
    StrsDict(add=vocab).update()
    SylDict(add=vocab).update()
    RhymDict(add=vocab).update()
