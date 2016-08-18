from nltk import *
from re import findall
from settings import Settings

file_ext = '/users/jason/teknopoetx/tmp/'


def file_num():
    import json
    with open('j_son/file_iter.json') as f_iter: start = json.load(f_iter)
    f_num = iter(range(start, 1000000))
    next(f_num)
    last = next(f_num)
    with open('j_son/file_iter.json', 'w') as f_itr: json.dump(last, f_itr)
    return str(last)


def reset_iter():
    import json
    reset = iter(range(1000000))
    last = next(reset)
    with open('j_son/file_iter.json', 'w') as f_itr: json.dump(last, f_itr)
    print(last)
    return str(last)


def sentlines(text_name):
    file = open(text_name)
    text_lines = file.readlines()
    file.close()
    text_list = []
    for txt in text_lines:
        txt = txt.lstrip()
        txt = txt.replace('\n', '')
        txt = txt.rstrip()
        text_list.append(txt)
    text_sent_lines = []
    for line in text_list:
        word_line = wordpunct_tokenize(line)
        if word_line:
            if word_line[0] == '\ufeff':
                word_line.remove('\ufeff')
        text_sent_lines.append(word_line)
    return text_sent_lines


def word_split(text_name):
    text_list = []
    textlines = open(text_name).readlines()
    for line in textlines:
        txt = line.split()
        text_list.append(txt)
    return text_list


def fix_quotes(textlist):
    fixed_list = []
    for line in textlist:
        thes = [w for w in line if findall(r'^[Tt][h][\']$', w)]
        apos = [w for w in line if findall(r'^[A-Za-z]+[\'][A-Za-z]+$', w)]
        apos2 = [w for w in line if findall(r'^[A-Za-z]+[’][A-Za-z]+$', w)]
        beg_qs = [w for w in line if findall(r'^[\'].*$', w)]
        end_qs = [w for w in line if findall(r'^.*[\']$', w)]
        beg_qd1 = [w for w in line if findall(r'^[\"].*$', w)]
        beg_qd2 = [w for w in line if findall(r'^[“].*$', w)]
        end_qd1 = [w for w in line if findall(r'^.*[\"]$', w)]
        end_qd2 = [w for w in line if findall(r'^.*[”]$', w)]
        for word in line:
            if word in thes:
                line[line.index(word)] = word.replace("'", "e")
            elif word in apos:
                line[line.index(word)] = word.replace("'", "~")
            elif word in apos2:
                line[line.index(word)] = word.replace("’", "~")
            elif word in beg_qs:
                line[line.index(word)] = word.replace("'", "{")
            elif word in end_qs:
                line[line.index(word)] = word.replace("'", "}")
            elif word in beg_qd1:
                line[line.index(word)] = word.replace('"', "[[")
            elif word in beg_qd2:
                line[line.index(word)] = word.replace('“', "[[")
            elif word in end_qd1:
                line[line.index(word)] = word.replace('"', "]]")
            elif word in end_qd2:
                line[line.index(word)] = word.replace('”', "]]")
        fixed = ' '.join(line)
        fixed_list.append(fixed)
    return fixed_list


def lower_case(textlist):
    lowered = []
    for elem in textlist:
        if isinstance(elem, str):
            lowered.append(elem.lower())
        else:
            sents = []
            for word in elem:
                sents.append(word.lower())
            lowered.append(sents)
    return lowered


def remove_punct(wordlist):
    just_words = []
    for word in wordlist:
        if word.isalpha() and ((len(word) > 1) or (word in ['i', 'a'])):
            just_words.append(word)
    return just_words


def sent_form(txt, frm):
    sent_str = ' '.join(txt)
    out_sent = sent_str[:]
    if sent_str:
        if frm:
            out_sent = sent_str[0].capitalize() + sent_str[1:]
    out_sent = out_sent.replace(' ,', ',')
    out_sent = out_sent.replace(' .', '.')
    out_sent = out_sent.replace(' ;', ';')
    out_sent = out_sent.replace(' :', ':')
    out_sent = out_sent.replace(' !', '!')
    out_sent = out_sent.replace(' ?', '?')
    out_sent = out_sent.replace(' - ', '-')
    out_sent = out_sent.replace(' -- ', '--')
    out_sent = out_sent.replace(' )', ')')
    out_sent = out_sent.replace('( ', '(')
    out_sent = out_sent.replace(' ]', ']')
    out_sent = out_sent.replace('[ ', '[')
    out_sent = out_sent.replace(' i ', ' I ')
    out_sent = out_sent.replace('{ ', "'")
    out_sent = out_sent.replace(' }', "'")
    out_sent = out_sent.replace(' {', " '")
    out_sent = out_sent.replace('} ', "' ")
    out_sent = out_sent.replace('.}', ".'")
    out_sent = out_sent.replace(',}', ",'")
    out_sent = out_sent.replace('[[ ', '"')
    out_sent = out_sent.replace(' ]]', '"')
    out_sent = out_sent.replace(' [[', ' "')
    out_sent = out_sent.replace(']] ', '" ')
    out_sent = out_sent.replace('.]]', '."')
    out_sent = out_sent.replace(',]]', ',"')
    out_sent = out_sent.replace('[[', '"')
    out_sent = out_sent.replace(']]', '"')
    out_sent = out_sent.replace(" ~ ", "'")
    out_sent = out_sent.replace(' ".', '".')
    out_sent = out_sent.replace('. ', '.  ')
    out_sent = out_sent.replace(' ’ ', "'")
    out_sent = out_sent.replace(" ' d", "'d")
    out_sent = out_sent.replace(" ' s ", "'s ")
    out_sent = out_sent.replace("o ' er", "over")
    out_sent = out_sent.replace(" ne'er ", " never ")
    out_sent = out_sent.replace("'d", "ed")
    out_sent = out_sent.replace("'st", "")
    return out_sent


def rem_blnklines(file, file_id):
    outfilen = file_ext + file_id + '.txt'
    for line in open(file):
        if line != '\n':
            open(outfilen, 'a').write(line)
            open(outfilen, 'a').close()


def format_text(file, file_id, sett, frm=''):
    sent_lines = gen_form(sett, file)
    formatted = ''
    for line in sent_lines:
        f_line = sent_form(line, frm) + '\n'
        f = open('process/procd/' + file_id + '_procd.txt', 'a')
        f.write(f_line)
        f.close()
        formatted += f_line
    return formatted


def gen_form(sett, txt=''):
    if txt:
        source = txt
    else:
        source = sett.srce_txt
    formatted = []
    spl_txt = word_split(source)
    text_lst = fix_quotes(spl_txt)
    for txt in text_lst:
        txt = txt.lstrip()
        txt = txt.rstrip()
        if txt in [w for w in text_lst if re.findall(r'^[ivxlcIVXLC]+[\.]$', w)
        and w not in ['I', 'i', 'Ill', 'ill', 'civil', 'Civil']]:
            formatted.append('\n')
        else:
            formatted.append(txt)
    text_sent_lines = []
    for line in formatted:
        word_line = wordpunct_tokenize(line)
        if word_line:
            if word_line[0] == '\ufeff':
                word_line.remove('\ufeff')
        text_sent_lines.append(word_line)
    return text_sent_lines


if __name__ == '__main__':
    mset = Settings()
    format_text('process/shakespeare-sonnets2.txt', 'shks2', mset)

    '''
    for n in range(1,50):
        filen1 = '/users/jason/python/digital_poetry/logs/js_poems/log-js_poems'+str(n)+'.txt'
        filen2 = '/users/jason/python/digital_poetry/logs/js_poems/js_poems'+str(n)+'.txt'
        for line in open(filen1):
            if line != '\n':
                open(filen2, 'a').write(line)
        f = open(filen2)
        poems = f.read().split('* * *')
        count = 1
        for poem in poems:
            file3 = '/users/jason/python/digital_poetry/logs/js_poems/poems/'+str(count)+'_poems0.txt'
            open(file3, 'a').write('\n* * *\n' + poem)
            count += 1

    '''
