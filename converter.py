from StringIO import StringIO
import codecs
import markdown
import os

from markdown_checklist.extension import ChecklistExtension
from markdown.extensions.nl2br import Nl2BrExtension
from markdown.extensions.toc import TocExtension
#from markdown_newtab import NewTabExtension
# new tab is great but overzealous on internal links

type2ext = {
        'md': ['.md', '.wiki'],
        'txt': ['.txt'],
        'none': ['.html']
    }

def getType(filename):
    file, ext = os.path.splitext(filename)
    for type, extensions in type2ext.iteritems():
        if ext in extensions:
            return type
    return None

def getConvertableTypeExtensions():
    def flatten(accum, x):
        accum.extend(x)
        return accum
    r = reduce(flatten, type2ext.values(), [])
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



extensions=[
        TocExtension(title='Table of Contents'),
        ChecklistExtension(),
        Nl2BrExtension()
        #NewTabExtension()
        ]

def markdown2html(in_str):
    return markdown.markdown(in_str, output_format='html5', extensions=extensions)

def txt2html(in_str):
    return in_str.replace('\n', '<br/>')
