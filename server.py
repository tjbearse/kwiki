import flask
import markdown
import converter
import os
import datetime

app = flask.Flask(__name__)
app.config['DEBUG'] = True

app.config['root'] = os.getcwd()

WIKI = 'wiki'
NON_WIKI = 'file'
DIR = 'dir'

@app.route('/wiki/', defaults={'path': './'}, methods=['GET', 'POST'])
@app.route('/wiki/<path:path>', methods=['GET', 'POST'])
def fileDispatch(path):
    if '..' in path:
        print '.. in path'
        abort(404)

    fullpath = flask.safe_join(app.config['root'], path)
    #path = '/' + path
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
        if flask.request.args.get('directory') is None:
            index = findIndex(fullpath, path)
            if index:
                return flask.redirect(
                        flask.url_for('fileDispatch', path=index)
                    )
        return listing(fullpath, path, crumbs)

    else:
        if flask.request.method == 'POST':
            abort(500)
        # list override?
        context, file = os.path.split(fullpath)
        # try w/o extension
        file, ext = os.path.splitext(path)
        if ext == '':
            for ext in converter.getConvertableTypeExtensions():
                if os.path.exists(fullpath + ext):
                    return flask.redirect(
                            flask.url_for('fileDispatch', path=path + ext)
                        )
        print 'fileDispatch', path, fullpath
        flask.abort(404)

def findIndex(fullpath, route):
    for ext in converter.getConvertableTypeExtensions():
        ipath = flask.safe_join(fullpath, 'index' + ext)
        if os.path.exists(ipath):
            return flask.safe_join(route, 'index' + ext)
    return None

# req full path
def getFileType(path):
    if os.path.isfile(path):
        file, ext = os.path.splitext(path)
        if(ext in converter.getConvertableTypeExtensions()):
            return WIKI
        else:
            return NON_WIKI
    elif os.path.exists(path):
        return DIR
    else:
        return None

def notMarkdown(path):
    return flask.send_file(path)

def processWikiRequest(fullpath, crumbs):
    raw = None
    if flask.request.method == 'POST':
        raw = flask.request.form.get('raw')

    if flask.request.args.get('edit') is not None:
        template = 'edit-document.html'
    else:
        if flask.request.method == 'POST':
            if raw is not None:
                print "writing {} with {}".format(fullpath, raw)
                with open(fullpath, 'w') as f:
                    f.write(raw)
            else:
                abort(400)
        template = 'document.html'

    if raw is not None:
        type = converter.getType(fullpath)
        html = flask.Markup(converter.convert(raw, type))
    else:
        html, raw = converter.convertFromFile(fullpath)
        html = flask.Markup(html)
    return flask.render_template(template,
                content=html,
                crumbs=crumbs,
                raw=raw
            )

def listing(directory, route, crumbs):
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
    stat = os.stat(fullpath)
    size = stat.st_size
    time = stat.st_mtime
    # human readable date
    for pre in ['B', 'KB', 'GB']:
        if size < 1024:
            size = str(size) + ' ' + pre
            break
        size /= 1024
    # human readable time
    time = datetime.datetime.utcfromtimestamp(time)
    basename = os.path.basename(file)
    title, ext = os.path.splitext(basename)
    return {
            "title": title,
            "basename": basename,
            "href": flask.safe_join(relRoute, file),
            "humansize": size,
            "humantime": time
        }

"""
"crumbs": [("index", "/"), ("some-document", None)]
"""
def makeLink(wikipath):
    if wikipath is not None:
        url =flask.safe_join('/wiki', wikipath)
    else:
        url = None
    return url
# relative route path
def buildCrumbs(path):
    crumbs = []
    prepath = None
    path, elt = os.path.split(path)
    while elt != "":
        url = makeLink(prepath)
        crumbs.append((elt, url))
        prepath = path
        path, elt = os.path.split(path)
    if elt == "":
        url = makeLink(prepath)
        crumbs.append(('home', url))
    crumbs.reverse()
    return crumbs



@app.errorhandler(404)
def page_not_found(e):
    print e
    return flask.render_template('404.html'), 404

if __name__ == '__main__':
    app.run()

