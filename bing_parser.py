from lxml.html import fromstring


def to_text(el):
    if len(el) == 1:
        return el[0].text_content()
    else:
        return ''


def bing_html_parser(html):
    tree = fromstring(html)
    word_data = {}
    try:
        qdef = tree.cssselect('div.qdef')[0]
        # 简单释义
        hd_area = qdef.find_class('hd_area')[0]
        word = hd_area.find_class('hd_div')
        hd_prus = hd_area.find_class('hd_prUS')
        hd_pr = hd_area.find_class('hd_pr')
        hd_if = qdef.find_class('hd_if')
        lis = qdef.findall('ul/li')
        word_data['word'] = to_text(word)
        word_data['pr-us'] = to_text(hd_prus)
        word_data['pr-uk'] = to_text(hd_pr)
        word_data['inflection'] = to_text(hd_if)
        word_data['short-def'] = []
        for li in lis:
            pos = li.find_class('pos')
            ele_def = li.find_class('def')
            li_data = {'pos': to_text(pos), 'def': to_text(ele_def)}
            word_data['short-def'].append(li_data)
        # 详细释义
        auth_area = tree.cssselect('div.auth_area')[0]
        each_segs = auth_area.find_class('each_seg')
        word_data['long-def'] = []
        for each_seg in each_segs:
            seg_data = {}
            pos = each_seg.find_class('pos')
            seg_data['pos'] = to_text(pos)
            seg_data['li-datas'] = []
            de_seg = each_seg.find_class('de_seg')[0]
            for li in de_seg.getchildren():
                li_data = {}
                ele_class = li.attrib['class']
                if ele_class == 'se_lis':
                    li_data['type'] = 'sense'
                elif ele_class == 'li_exs':
                    li_data['type'] = 'example'
                else:
                    li_data['type'] = 'unk'
                li_data['row-datas'] = []
                def_rows = li.find_class('def_row')
                if li_data['type'] == 'sense':
                    for def_row in def_rows:
                        row_data = {}
                        se_d = def_row.find_class('se_d')
                        gram_grp = def_row.find_class('au_def')
                        sen_com = def_row.find_class('sen_com')
                        bil = def_row.find_class('bil')
                        val = def_row.find_class('val')
                        row_data['sen-idx'] = to_text(se_d)
                        row_data['gram-grp'] = to_text(gram_grp)
                        row_data['sen-com'] = to_text(sen_com)
                        row_data['bil'] = to_text(bil)
                        row_data['val'] = to_text(val)
                        li_data['row-datas'].append(row_data)
                elif li_data['type'] == 'example':
                    for def_row in def_rows:
                        row_data = {}
                        val_ex = def_row.find_class('val_ex')
                        bil_ex = def_row.find_class('bil_ex')
                        row_data['val_ex'] = to_text(val_ex)
                        row_data['bil_ex'] = to_text(bil_ex)
                        li_data['row-datas'].append(row_data)
                seg_data['li-datas'].append(li_data)
            word_data['long-def'].append(seg_data)
    except IndexError:
        print('not completed!')
    return word_data
