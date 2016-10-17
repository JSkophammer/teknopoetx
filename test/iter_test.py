
import json

def file_num():
    #with open('json/iter.json') as f_iter: start = json.load(f_iter)
    I = iter(range(1000000))
    #next(I)
    last = next(I)
    with open('json/iter.json', 'w') as f_itr: json.dump(last, f_itr)
    return str(last)

print(file_num())
