import flask
import os

import converter
import fileOps
import searchEngine
import urlconverters

app = flask.Flask(__name__)

app.url_map.converters['dir'] = urlconverters.DirectoryConverter
app.url_map.converters['wiki'] = urlconverters.getFileConverter(
        includeByDefault = False,
        exceptions = converter.getConvertableTypeExtensions()
    )
app.url_map.converters['file'] = urlconverters.getFileConverter(
        includeByDefault = True,
        exceptions = converter.getConvertableTypeExtensions()
    )

app.config['DEBUG'] = True

app.config['root'] = os.getcwd()

@app.route('/wiki/<dir:path>', methods=['GET', 'POST'])
@app.route('/wiki/<file:path>', methods=['GET', 'POST'])
@app.route('/wiki/<wiki:path>', methods=['GET', 'POST'])
@app.route('/wiki/', defaults={'path': ''}, methods=['GET', 'POST'])
def fileDispatch(path):
    if '..' in path:
        print '.. in path'
        abort(404)

    fullpath = flask.safe_join(app.config['root'], path)
    type = fileOps.getFileType(fullpath)
    crumbs = fileOps.buildCrumbs(path)
    if type == fileOps.WIKI:
        return processWikiRequest(fullpath, crumbs)


    elif type == fileOps.NON_WIKI:
        if flask.request.method == 'POST':
            abort(500)
        return notMarkdown(fullpath)

    elif type == fileOps.DIR:
        if path != '' and path[-1] != '/':
            return flask.redirect(flask.url_for('fileDispatch', path=path+'/'))
        if flask.request.method == 'POST':
            abort(500)
        # try index
        if flask.request.args.get('directory') is None:
            index = fileOps.findIndex(fullpath, path)
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
    pages = []
    files = []
    subdirs = []
    for f in os.listdir(directory):
        if f[0] == '.':
            continue
        fullpath = flask.safe_join(directory, f)
        ftype = fileOps.getFileType(fullpath)
        if ftype == fileOps.WIKI:
            pages.append(fileOps.getFileInfo(f, fullpath, route))
        elif ftype == fileOps.NON_WIKI:
            files.append(fileOps.getFileInfo(f, fullpath, route))
        else:
            subdirs.append(fileOps.getDirInfo(f, route))

    return flask.render_template('listing.html',
            crumbs=crumbs,
            directory=os.path.basename(directory),
            files=files,
            pages=pages,
            sub_directories=subdirs
            )

@app.route('/search', methods=['GET', 'POST'])
def search():
    results = []
    search = flask.request.form.get('q')
    if search is not None:
        results = searchEngine.search(search)
    return flask.render_template('search.html', query=search, results=results)


@app.errorhandler(404)
def page_not_found(e):
    print e
    return flask.render_template('404.html'), 404

if __name__ == '__main__':
    app.run()

