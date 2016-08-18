import json


class Settings:
    def __init__(self):
        # Set file paths for texts used in techno_poet.gen_text
        self.txt_name = 'process/procd/shks2_procd.txt'
        self.rvg_name = 'js3_rg'
        self.file_idn = 'js_shks'
        self.log_fldr = 'sonnets'
        self.txt_frmt = 'poem'  # Set format to 'poem' to capitalize beginning of lines
        self.iter_num = 1  # Set number of output texts to generate
        self.sylc = True
        self.strs = True
        self.rhym = True
        self.alit = False

        # Set main file path
        self.file_pth = '/Users/Jason/Programming/GitHub/Teknopoetx/teknopoetx'
        self.tmp_file = self.file_pth + 'tmp/tmp_file.txt'
        self.srce_txt = self.file_pth + self.txt_name
        self.log_file = self.file_pth + 'logs/' + self.log_fldr + '/' + self.file_idn
        self.main_id = self.file_pth + 'j_son/main_gram.json'
        self.vocb_id = self.file_pth + 'j_son/main_vocb.json'
        self.rgrm_id = self.file_pth + 'j_son/mrev_gram.json'
        self.mgrm_id = self.file_pth + 'j_son/main_gram.json'
        self.pron_id = self.file_pth + 'j_son/pron_dict.json'
        self.strs_id = self.file_pth + 'j_son/strs_dict.json'
        self.sylc_id = self.file_pth + 'j_son/syl_count.json'
        self.rhym_id = self.file_pth + 'j_son/rhym_dict.json'

        self.grm_strc = json.load(open(self.file_pth + 'j_son/gram_strc/pdl_grmstrc.json'))
        self.frev_grm = json.load(open(self.file_pth + 'j_son/rev_gram/' + self.rvg_name + '.json'))

        # Open main dictionaries used in programs
        self.main_vocb = json.load(open(self.vocb_id))
        self.pron_dict = json.load(open(self.pron_id))
        self.rhym_dict = json.load(open(self.rhym_id))
        self.strs_dict = json.load(open(self.strs_id))
        self.syl_count = json.load(open(self.sylc_id))
        self.main_gram = json.load(open(self.mgrm_id))
        self.mrev_gram = json.load(open(self.rgrm_id))

        # Open auxiliary files
        self.freq_pron = json.load(open(self.file_pth + 'j_son/freq_pron.json'))
        self.cmu_vocab = json.load(open(self.file_pth + 'j_son/cmu_vocab.json'))
        self.brwn_vocb = json.load(open(self.file_pth + 'j_son/brwn_vocb.json'))
        self.stnd_vocb = json.load(open(self.file_pth + 'j_son/stnd_vocb.json'))
        self.brwn_dict = json.load(open(self.file_pth + 'j_son/brwn_dict.json'))
        self.cmu_pdict = json.load(open(self.file_pth + 'j_son/cmu_pdict.json'))
        self.eng_words = json.load(open(self.file_pth + 'j_son/eng_words.json'))
        self.stp_words = json.load(open(self.file_pth + 'j_son/stp_words.json'))
