import sys
from downloader import Downloader
from bing_parser import bing_html_parser

# url = 'http://dict.youdao.com/search'
url = 'https://cn.bing.com/dict/search'
params = {'q': ' '.join(sys.argv[1:])}
dler = Downloader()
html = dler(url, params)
bing_html_parser(html)
