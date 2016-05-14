from StringIO import StringIO
import markdown
import markdown.extensions.toc
from markdown_checklist.extension import ChecklistExtension




extensions=[
        markdown.extensions.toc.TocExtension(title='Table of Contents'),
        ChecklistExtension()
        ]

def markdown2html(in_str):
    return markdown.markdown(in_str, extensions=extensions)

