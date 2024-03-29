import flask
import os
import datetime
from werkzeug.utils import safe_join

import converter

WIKI = 'wiki'
NON_WIKI = 'file'
DIR = 'dir'

def findIndex(fullpath, route):
    for ext in converter.getConvertableTypeExtensions():
        ipath = safe_join(fullpath, 'index' + ext)
        if os.path.exists(ipath):
            return safe_join(route, 'index' + ext)
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

def getDirInfo(d, relRoute):
    path = safe_join(relRoute, d)
    return {
            "basename": d,
            "href": flask.url_for('fileDispatch', path=path)
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
            "href": flask.url_for('fileDispatch', path=safe_join(relRoute, file)),
            "humansize": size,
            "humantime": time
        }

def makeLink(wikipath):
    if wikipath is not None:
        url =flask.url_for('fileDispatch', path=wikipath)
    else:
        url = None
    return url
# relative route path
def buildCrumbs(path):
    crumbs = []
    prepath = None
    path, elt = os.path.split(path)
    if elt == "":
        path, elt = os.path.split(path)
    while elt != '':
        url = makeLink(prepath)
        crumbs.append((elt, url))
        prepath = path
        path, elt = os.path.split(path)
    if elt == "":
        url = makeLink(prepath)
        crumbs.append(('home', url))
    crumbs.reverse()
    return crumbs


