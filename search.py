import sys
import json
from downloader import Downloader
# from bing_parser import bing_html_parser
from youdao_parser import youdao_html_parser

url = 'http://dict.youdao.com/search'
# url = 'https://cn.bing.com/dict/search'
params = {'q': ' '.join(sys.argv[1:])}
dler = Downloader()
html = dler(url, params)
word_data = youdao_html_parser(html)
with open('word-data.json', mode='w', encoding='utf-8') as f:
    json.dump(word_data, f, ensure_ascii=False, indent=2)
