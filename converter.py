import codecs
import flask
import jinja2
import markdown
import os

from markdown_checklist.extension import ChecklistExtension
from markdown.extensions.nl2br import Nl2BrExtension
from markdown.extensions.toc import TocExtension
from functools import reduce
#from markdown_newtab import NewTabExtension
# new tab is great but overzealous on internal links

type2ext = {
        'md': ['.md', '.wiki'],
        'txt': ['.txt', '.org'],
        'none': ['.html']
    }

def getType(filename):
    file, ext = os.path.splitext(filename)
    for type, extensions in type2ext.items():
        if ext in extensions:
            return type
    return None

def getConvertableTypeExtensions():
    def flatten(accum, x):
        accum.extend(x)
        return accum
    r = reduce(flatten, list(type2ext.values()), [])
    return r



def convert(in_str, type):
    if type == 'md':
        return markdown2html(in_str)
    elif type == 'txt':
        return txt2html(in_str)
    elif type == 'none':
        return in_str
    else:
        raise 'no type'

def convertFromFile(file):
    type = getType(file)
    with codecs.open(file, 'r', encoding='utf-8') as f:
        raw = f.read()
        html = convert(raw, type)
    return html, raw


# copied from checklist extension and wrap text in span, allows styling checked / unchecked text
def render_checklist_item(caption, checked):
    checked = ' checked' if checked else ''
    return '<li><input type="checkbox" disabled%s><span>%s</span></li>' % (checked, caption)

extensions=[
        TocExtension(title='Table of Contents'),
        ChecklistExtension(render_item=render_checklist_item),
        Nl2BrExtension(),
        'markdown.extensions.tables'
        #NewTabExtension()
        ]

def markdown2html(in_str):
    # preprocess templating in the markdown text first
    try:
        in_str = flask.render_template_string(in_str)
    except jinja2.exceptions.TemplateSyntaxError as error:
        return '!!! error in jinja template: {}'.format(error)

    return markdown.markdown(in_str, output_format='html5', extensions=extensions)

def txt2html(in_str):
    return in_str.replace('\n', '<br/>')
