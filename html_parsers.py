from lxml.html import fromstring


def get_text(element):
    if element is not None:
        import re
        text = element.text_content()
        text = re.sub(r'([\t\n])+', '', text)
        text = re.sub(r'\s{2,}', ' ', text)
        return text.strip()
    else:
        return ''


def parser_youdao(html):
    tree = fromstring(html)
    word_data = {}
    try:
        results_contents = tree.xpath('//div[@id="results-contents"]')
        if len(results_contents) != 1:
            return word_data
        results_contents = results_contents[0]

        # 简单释义
        phrs_list_tab = results_contents.find('div[@id="phrsListTab"]')
        if phrs_list_tab is None:
            return word_data
        word = phrs_list_tab.find('h2/span[@class="keyword"]')
        pronounces = phrs_list_tab.findall('h2/div/span[@class="pronounce"]')
        short_list = phrs_list_tab.findall('div[@class="trans-container"]/ul/li')
        word_data['word'] = get_text(word)
        word_data['pronounces'] = []
        word_data['short-list'] = []
        for pronounce in pronounces:
            if pronounce.find('span[@class="phonetic"]') is not None:
                word_data['pronounces'].append(get_text(pronounce))
        for li in short_list:
            word_data['short-list'].append(get_text(li))

        # 详细释义
        collins_result = results_contents.find('.//div[@id="collinsResult"]')
        if collins_result is None:
            return word_data
        rank = collins_result.find('.//span[@class="via rank"]')
        additional_pattern = collins_result.find('.//span[@class="additional pattern"]')
        long_list = collins_result.findall('.//ul[@class="ol"]/li')

        word_data['rank'] = get_text(rank)
        word_data['inflection'] = get_text(additional_pattern)
        word_data['long-list'] = []
        for li in long_list:
            collins_major_trans = li.find('.//div[@class="collinsMajorTrans"]')
            if collins_major_trans is None:
                continue
            collins_order = collins_major_trans.find('.//span[@class="collinsOrder"]')
            part_of_speech = collins_major_trans.find('.//span[@class="additional"]')
            major_trans = collins_major_trans.find('p')
            li_data = {'collins-order': get_text(collins_order),
                       'part-of-speech': get_text(part_of_speech),
                       'major-trans': get_text(major_trans),
                       'examples': []}
            example_lists = li.findall('.//div[@class="exampleLists"]')
            for example in example_lists:
                exs = example.findall('.//div[@class="examples"]/p')
                exs_li = []
                for ex in exs:
                    exs_li.append(get_text(ex))
                li_data['examples'].append(exs_li)
            word_data['long-list'].append(li_data)
    except IndexError:
        print('not completed!')
    return word_data
