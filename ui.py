import json
import time
from prompt_toolkit import Application
from prompt_toolkit.buffer import Buffer
from prompt_toolkit.layout.containers import HSplit, VSplit, Window
from prompt_toolkit.layout.controls import BufferControl, FormattedTextControl
from prompt_toolkit.layout.layout import Layout
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.widgets import TextArea, SearchToolbar, Frame, VerticalLine, HorizontalLine
from prompt_toolkit.styles import Style
from prompt_toolkit.document import Document
from downloader import Downloader
from html_parsers import parser_youdao

kb = KeyBindings()


@kb.add('c-q')
def _exit_(event):
    event.app.exit()


@kb.add('c-i')
def _search_field_(event):
    event.app.layout.focus(search_field)


@kb.add('c-o')
def _search_result_(event):
    event.app.layout.focus(search_result)


def accept(buff):
    # Evaluate "calculator" expression.
    try:
        word = search_field.text
        url = 'http://dict.youdao.com/search?q='
        parser = parser_youdao
        dler = Downloader()
        t0 = time.time()
        html = dler(url + word, word)
        t1 = time.time()
        t2 = time.time()
        word_data = parser(html)
        t3 = time.time()
        message = f'download cost {t1 - t0}s parse cost {t3 - t2}s'
        output = json.dumps(word_data, ensure_ascii=False, indent=4)
    except BaseException as e:
        output = '\n\n{}'.format(e)
        message = '\n\n{}'.format(e)
    new_text = output
    search_result.buffer.document = Document(text=new_text, cursor_position=0)
    personal_content.buffer.document = Document(text=message, cursor_position=0)


search_result = TextArea(text='results')
personal_content = TextArea(text='personal content')
future_content = TextArea(text='reserve content')
search_field = TextArea(height=1, prompt='search: ', multiline=False, wrap_lines=False)
body_container = VSplit([search_result,
                         VerticalLine(),
                         HSplit([personal_content,
                                 HorizontalLine(),
                                 future_content])])
root_container = HSplit([body_container,
                         HorizontalLine(),
                         search_field])
search_field.accept_handler = accept
layout = Layout(root_container, focused_element=search_field)
app = Application(layout=layout, full_screen=True, key_bindings=kb)
app.run()
