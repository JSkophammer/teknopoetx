from time import ctime
from txt_admin import *
from settings1 import Settings

start = ctime()
print('Start:', start)
#sett = Settings()


class PoemGen:
    def __init__(self):
        self.anlz = Anlyz()
        self.sett = Settings()
        self.sylc = self.sett.sylc
        self.strs = self.sett.strs
        self.rhym = self.sett.rhym
        self.alit = self.sett.alit
        self.grm_fnct = self.anlz.gram_struc
        self.rev_gram = self.sett.mrev_gram
        self.syl_file = self.sett.syl_count
        self.str_file = self.sett.strs_dict
        self.rhy_file = self.sett.rhym_dict
        self.prn_file = self.sett.pron_dict

    def filter_select(self, word, pos, rhyme, sett):
        filtr = sett.frev_grm[pos]
        filters = []
        if self.sylc:
            filtr = [w for w in filtr if self.syl_file[w] == self.syl_file[word]]
            filters.append(filtr)
        if self.strs:
            filtr = [w for w in filtr if self.str_file[w] == self.str_file[word]]
            filters.append(filtr)
        if self.alit:
            filtr = [w for w in filtr if self.prn_file[w][0] == self.prn_file[word][0]]
            filters.append(filtr)
        if rhyme:
            filtr = [w for w in filtr if self.rhy_file[w] == self.rhy_file[word]]
            if not filtr:
                filtr = [word]
            filters.append(filtr)
        final = []
        i = 0
        while i < len(filters) and filters[i]:
            final = filters[i]
            i += 1
        if not final:
            final = [word]
        return final

    def choose_words(self, line, sett):
        stp_wrds = self.sett.stp_words + ['o', 'O']
        mad_lib = []
        for i in range(len(line)):
            gen_word = line[i].lower()
            grm_sent = self.grm_fnct(line)
            if gen_word not in stp_wrds and grm_sent[i] in sett.frev_grm.keys() and gen_word.isalpha():
                if gen_word == line[-1] or (not line[-1].isalpha() and gen_word == line[-2].lower()):
                    rand_word = choice(self.filter_select(gen_word, grm_sent[i], True, sett))
                else:
                    rand_word = choice(self.filter_select(gen_word, grm_sent[i], False, sett))
                mad_lib.append(rand_word)
            else:
                mad_lib.append(gen_word)
        return mad_lib

    def gen_text(self):
        if self.sett.new_text:
            Vocab(self.sett.text_idn).generate(self.sett.txt_name)
            update_all(self.sett.text_vocb)
        sent_lines = sentlines(self.sett.txt_name)
        count = 0
        while count < self.sett.iter_num:
            rand_log = ''
            if self.sett.rvg_rand:
                mset = Settings()
                rand_log = mset.rand_rvg()
            else:
                mset = self.sett
            if self.sett.num_file:
                f_num = file_num()
                fl_rw = 'w'
            else:
                f_num = ''
                fl_rw = 'a'
            log_text = ''
            for i in range(len(sent_lines)):
                if self.sett.lin_rand:
                    mset = Settings()
                    rand_log += '\n' + str(i + 1) + ': ' + mset.rand_rvg()
                print(sent_form(sent_lines[i], self.sett.txt_frmt))
                mad_sen = sent_form(self.choose_words(sent_lines[i], mset), self.sett.txt_frmt)
                log_text += (mad_sen + '\n')
            with open(self.sett.log_file + f_num + '.txt', fl_rw) as f:
                f.write(log_text + '\n' + rand_log + '\n\n')
            count += 1
        end = ctime()
        print(anlz.time_elapse(start, end))


if __name__ == '__main__':
    # reset_iter()
    PoemGen().gen_text()
