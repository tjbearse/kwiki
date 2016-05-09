from StringIO import StringIO
import flask
import markdown
import os

app = flask.Flask(__name__)
app.config['DEBUG'] = True

app.config['wikiExt'] = ['.md', '.wiki']
app.config['markdownSettings'] = {}
app.config['root'] = os.getcwd()

WIKI = 'wiki'
NON_WIKI = 'file'
DIR = 'dir'

@app.route('/', defaults={'path': './'})
@app.route('/<path:path>')
def fileDispatch(path):
    if '..' in path or path.startswith('/'):
        abort(404)

    fullpath = flask.safe_join(app.config['root'], path)
    type = getFileType(fullpath)
    if(type == WIKI):
        return markdownFile(fullpath, '/'+path)
    elif(type == NON_WIKI):
        return notMarkdown(fullpath)
    else:
        return listing(fullpath, '/'+path)

# req full path
def getFileType(path):
    if(os.path.isfile(path)):
        file, ext = os.path.splitext(path)
        if(ext in app.config['wikiExt']):
            return WIKI
        else:
            return NON_WIKI
    else:
        return DIR

def notMarkdown(path):
    return flask.send_file(path)

"""
{
  "content": "<h1>...", # The XHTML for the document.
  "title": "Some Document", # The extracted title of the document.
  "crumbs": [("index", "/"), ("some-document", None)] # Breadcrumbs
}
"""
def markdownFile(wikipage, route):
    istream = StringIO()
    try:
        markdown.markdownFromFile(input=wikipage, output=istream, **app.config['markdownSettings'])
        md = flask.Markup(istream.getvalue())
        return flask.render_template('document.html',
                    content=md,
                    crumbs=buildCrumbs(route)
                )
    except Exception as e:
        print 'file failed', wikipage, e.args
        flask.abort(404)
    finally:
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
def listing(directory, route):
    print('directory', directory)
    try:
        pages = []
        files = []
        subdirs = []
        for f in os.listdir(directory):
            if f[0] == '.':
                continue
            fullpath = flask.safe_join(directory, f)
            ftype = getFileType(fullpath)
            if ftype == WIKI:
                pages.append(getFileInfo(f, fullpath, route))
            elif ftype == NON_WIKI:
                files.append(getFileInfo(f, fullpath, route))
            else:
                subdirs.append(getDirInfo(f, route))

        return flask.render_template('listing.html',
                crumbs=buildCrumbs(route),
                directory=os.path.basename(directory),
                files=files,
                pages=pages,
                sub_directories=subdirs
                )
    except Exception as e:
        print 'directory failed:', e
        flask.abort(404)

def getDirInfo(d, relRoute):
    return {
            "basename": d,
            "href": flask.safe_join(relRoute, d)
        }

def getFileInfo(file, fullpath, relRoute):
    basename = os.path.basename(file)
    title, ext = os.path.splitext(basename)
    return {
            "title": title,
            "basename": basename,
            "href": flask.safe_join(relRoute, file),
            #TODO
            "humansize": "?B",
            "size": "?",
            "slug": "example"
        }

"""
"crumbs": [("index", "/"), ("some-document", None)]
"""
# relative route path
def buildCrumbs(path):
    crumbs = []
    prepath = None
    path, elt = os.path.split(path)
    while elt != "":
        crumbs.append((elt, prepath))
        path, elt = os.path.split(path)
        prepath = path
    if elt == "":
        crumbs.append(('home', prepath))
    print crumbs
    crumbs.reverse()
    return crumbs



@app.errorhandler(404)
def page_not_found(e):
    return flask.render_template('404.html'), 404

if __name__ == '__main__':
    app.run()
