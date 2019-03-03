import re
from lxml.html import fromstring


def youdao_html_parser(html):
    # pattern = re.compile(r'(\n|\t|\s)+')
    tree = fromstring(html)
    word_data = {}
    try:
        results_contents = tree.xpath('//*[@id="results-contents"]')[0]
        # 上半部分的简单释义
        phrsListTab = results_contents.find('*[@id="phrsListTab"]')
        word = phrsListTab.find('h2/span')
        pronounce = phrsListTab.findall('h2/div/span')
        pronounce_en = pronounce[0].find('span')
        pronounce_us = pronounce[1].find('span')
        short_list = phrsListTab.findall('*[@class="trans-container"]/ul/li')

        word_data['word'] = word.text_content()
        word_data['pronounce_en'] = pronounce_en.text_content()
        word_data['pronounce_us'] = pronounce_us.text_content()
        word_data['short-list'] = []
        for li in short_list:
            word_data['short-list'].append(li.text_content())

        # 详细释义
        collinsResult = results_contents.find('.//*[@id="collinsResult"]')
        rank = collinsResult.find('.//*[@class="via rank"]')
        inflection = collinsResult.find('.//*[@class="additional pattern"]')
        long_list = collinsResult.findall('.//ul/li')

        word_data['rank'] = rank.text_content()
        word_data['inflection'] = inflection.text_content()
        word_data['long-list'] = []
        for li in long_list:
            collinsMajorTrans = li.find('.//*[@class="collinsMajorTrans"]')
            collinsOrder = collinsMajorTrans.find('.//*[@class="collinsOrder"]')
            additional = collinsMajorTrans.find('.//*[@class="additional"]')
            major_trans = collinsMajorTrans.find('.//p')
            li_data = {'collins-order': collinsOrder.text_content(),
                       'gram-grp': additional.text_content(),
                       'major-trans': major_trans.text_content(),
                       'examples': []}
            exampleLists = li.findall('.//*[@class="exampleLists"]')
            for example in exampleLists:
                example_en, example_ch = example.findall('.//*[@class="examples"]/p')
                li_data['examples'].append({'en': example_en.text_content(),
                                            'ch': example_ch.text_content()})

            word_data['long-list'].append(li_data)

    except IndexError:
        print('not completed!')
    return word_data
