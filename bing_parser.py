from lxml.html import fromstring


def to_text(el):
    if len(el) == 1:
        return el[0].text_content()
    else:
        return ''


def bing_html_parser(html):
    tree = fromstring(html)
    try:
        qdef = tree.cssselect('div.qdef')[0]
        # 头部
        hd_area = qdef.find_class('hd_area')[0]
        word = hd_area.find_class('hd_div')
        hd_prus = hd_area.find_class('hd_prUS')
        hd_pr = hd_area.find_class('hd_pr')

        print(f'{to_text(word)}\n'
              f'{to_text(hd_prus)} '
              f'{to_text(hd_pr)}')
        lis = qdef.findall('ul/li')
        for li in lis:
            pos = li.find_class('pos')
            ele_def = li.find_class('def')
            print(f'{to_text(pos)} {to_text(ele_def)}')
        hd_if = qdef.find_class('hd_if')
        print(f'{to_text(hd_if)}')
        # 权威英汉双解
        auth_area = tree.cssselect('div.auth_area')[0]
        each_segs = auth_area.find_class('each_seg')
        for each_seg in each_segs:
            pos = each_seg.find_class('pos')
            print(to_text(pos) + ' ' + '-' * 128)
            de_seg = each_seg.find_class('de_seg')[0]
            for li in de_seg.getchildren():
                ele_class = li.attrib['class']
                def_rows = li.find_class('def_row')
                for def_row in def_rows:
                    if ele_class == 'se_lis':
                        se_d = def_row.find_class('se_d')
                        au_def = def_row.find_class('au_def')
                        sen_com = def_row.find_class('sen_com')
                        bil = def_row.find_class('bil')
                        val = def_row.find_class('val')

                        print(f'{to_text(se_d)}'
                              f' {to_text(au_def)}'
                              f' {to_text(sen_com)}'
                              f' {to_text(bil)}'
                              f' {to_text(val)}')
                    elif ele_class == 'li_exs':
                        val_ex = def_row.find_class('val_ex')
                        bil_ex = def_row.find_class('bil_ex')
                        print(f'{to_text(val_ex)}\n{to_text(bil_ex)}')
    except IndexError:
        print('没有找到')
