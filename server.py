from StringIO import StringIO
import flask
import markdown
import os

app = flask.Flask(__name__)
app.config['DEBUG'] = True

app.config['wikiExt'] = ['.md', '.wiki', '']
app.config['markdown'] = {}
app.config['root'] = os.getcwd()

Markdown = markdown.Markdown(**app.config['markdown'])

@app.route('/', defaults={'path': './'})
@app.route('/<path:path>')
def file(path):
    if '..' in path or path.startswith('/'):
        abort(404)

    fullpath = flask.safe_join(app.config['root'], path)
    print('full', fullpath)
    if(os.path.isfile(fullpath)):
        file, ext = os.path.splitext(fullpath)
        if(ext in app.config['wikiExt']):
            return markdownFile(path)
        else:
            return notMarkdown(path)
    else:
        return listing(path)

def notMarkdown(path):
    return flask.send_file(path)

"""
{
  "content": "<h1>...", # The XHTML for the document.
  "title": "Some Document", # The extracted title of the document.
  "crumbs": [("index", "/"), ("some-document", None)] # Breadcrumbs
}
"""
def markdownFile(wikipage):
    istream = StringIO()
    try:
        Markdown.convertFile(input=wikipage, output=istream)
        md = flask.Markup(istream.getvalue())
        return flask.render_template('document.html', content=md)
    except Exception as e:
        print file, e
        flask.abort(404)
    finally:
        Markdown.reset()
        istream.close()

"""
{"directory": "somedir",
 "crumbs": [("index", "/"),
            ("somedir", "/somedir/"),
            (jinja2.Markup('<span class="list-crumb">list</span>'), None)],
 "files": [{"basename": "example.css",
            "href": "/example.css",
            "humansize": "27B",
            "size": 27,
            "slug": "example"}],
 "pages": [{"basename": "hello.html",
            "href": "/subdir/hello",
            "humansize": "268B",
            "size": 268,
            "slug": "hello",
            "title": u"Hello again."}],
 "sub_directories": [{"basename": "subdir", "href": "/subdir/"}]}
"""
def listing(directory):
    print('directory', directory)
    try:
        contents = os.listdir(directory)
        # sep files vs dirs
        # filter .stuff
        return flask.render_template('listing.html')
    except Exception as e:
        print contents, e
        flask.abort(404)

if __name__ == '__main__':
    app.run()
