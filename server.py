import flask
import markdown
import markdownConv
import os

app = flask.Flask(__name__)
app.config['DEBUG'] = True

app.config['wikiExt'] = ['.md', '.wiki', '.txt', '']
app.config['root'] = os.getcwd()

WIKI = 'wiki'
NON_WIKI = 'file'
DIR = 'dir'

@app.route('/', defaults={'path': './'}, methods=['GET', 'POST'])
@app.route('/<path:path>', methods=['GET', 'POST'])
def fileDispatch(path):
    if '..' in path:
        print '.. in path'
        abort(404)

    fullpath = flask.safe_join(app.config['root'], path)
    path = '/' + path
    type = getFileType(fullpath)
    crumbs = buildCrumbs(path)
    if type == WIKI:
        return processWikiRequest(fullpath, crumbs)


    elif type == NON_WIKI:
        if flask.request.method == 'POST':
            abort(500)
        return notMarkdown(fullpath)

    elif type == DIR:
        if flask.request.method == 'POST':
            abort(500)
        # try index
        index = findIndex(fullpath, path)
        if index:
            return flask.redirect(index)
        return listing(fullpath, path, crumbs)

    else:
        if flask.request.method == 'POST':
            abort(500)
        # list override?
        context, file = os.path.split(fullpath)
        if file == '_directory_':
            route, dir = os.path.split(path)
            return listing(context, route, crumbs)
        # try w/o extension
        file, ext = os.path.splitext(path)
        if ext == '':
            for ext in app.config['wikiExt']:
                if os.path.exists(fullpath + ext):
                    return flask.redirect(path + ext)
        print 'fileDispatch', path, fullpath
        flask.abort(404)

def findIndex(fullpath, route):
    for ext in app.config['wikiExt']:
        ipath = flask.safe_join(fullpath, 'index' + ext)
        if os.path.exists(ipath):
            return flask.safe_join(route, 'index' + ext)
    return None

# req full path
def getFileType(path):
    if os.path.isfile(path):
        file, ext = os.path.splitext(path)
        if(ext in app.config['wikiExt']):
            return WIKI
        else:
            return NON_WIKI
    elif os.path.exists(path):
        return DIR
    else:
        return None

def notMarkdown(path):
    return flask.send_file(path)

def markdownFile(wikipage):
    with open(wikipage, 'r') as f:
        rawmd = f.read()
        html = flask.Markup(markdownConv.markdown2html(rawmd))
    return html, rawmd

def processWikiRequest(fullpath, crumbs):
    if flask.request.args.get('edit') is not None:
        raw = None
        if flask.request.method == 'POST':
            raw = flask.request.form.get('raw')
        if raw is not None:
            html = flask.Markup(markdownConv.markdown2html(raw))
        else:
            html, raw = markdownFile(fullpath)
        return flask.render_template('edit-document.html',
                    content=html,
                    crumbs=crumbs,
                    raw=raw
                )
    else:
        if flask.request.method == 'POST':
            raw = flask.request.form.get('raw')
            if raw is not None:
                print "writing {} with {}".format(fullpath, raw)
                with open(fullpath, 'w') as f:
                    f.write(raw)
            else:
                abort(400)
            html = flask.Markup(markdownConv.markdown2html(raw))
        else:
            html, md = markdownFile(fullpath)
        return flask.render_template('document.html',
                    content=html,
                    crumbs=crumbs
                )

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
def listing(directory, route, crumbs):
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
                crumbs=crumbs,
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
        prepath = path
        path, elt = os.path.split(path)
    if elt == "":
        crumbs.append(('home', prepath))
    crumbs.reverse()
    return crumbs



@app.errorhandler(404)
def page_not_found(e):
    return flask.render_template('404.html'), 404

if __name__ == '__main__':
    app.run()

