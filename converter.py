from StringIO import StringIO
import markdown
import markdown.extensions.toc
import markdown.extensions.nl2br
import os
from markdown_checklist.extension import ChecklistExtension
#from markdown_newtab import NewTabExtension
# new tab is great but overzealous on internal links

type2ext = {
        'md': ['.md', '.wiki', ''],
        'none': ['.txt', '.html']
    }

def getType(filename):
    file, ext = os.path.splitext(filename)
    for type, extensions in type2ext.iteritems():
        if ext in extensions:
            print 'returning type', type
            return type
    return None

def getConvertableTypeExtensions():
    def flatten(accum, x):
        accum.extend(x)
        return accum
    return reduce(flatten, type2ext.values(), [])



def convert(in_str, type):
    if type == 'md':
        return markdown2html(in_str)
    elif type == 'none':
        return txt2html(in_str)
    else:
        raise 'no type'

def convertFromFile(file):
    type = getType(file)
    print 'type', type
    with open(file, 'r') as f:
        raw = f.read()
        html = convert(raw, type)
    return html, raw



extensions=[
        markdown.extensions.toc.TocExtension(title='Table of Contents'),
        ChecklistExtension(),
        markdown.extensions.nl2br.Nl2BrExtension()
        #NewTabExtension()
        ]

def markdown2html(in_str):
    return markdown.markdown(in_str, output_format='html5', extensions=extensions)

def txt2html(in_str):
    return in_str.replace('\n', '<br/>')
