import sys
import time
import json
from downloader import Downloader
from html_parsers import parser_youdao

word = ' '.join(sys.argv[1:])
url = 'http://dict.youdao.com/search?q='
parser = parser_youdao
dler = Downloader()
t0 = time.time()
html = dler(url + word, word)
t1 = time.time()
t2 = time.time()
word_data = parser(html)
t3 = time.time()
print(F'download cost {t1 - t0} s\tparse cost {t3 - t2}')
'''
with open('word-data.json', mode='w', encoding='utf-8') as f:
    json.dump(word_data, f, ensure_ascii=False, indent=2)
'''
print(json.dumps(word_data, ensure_ascii=False, indent=4))
