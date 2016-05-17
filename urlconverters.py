from werkzeug.routing import BaseConverter

class FileConverter(BaseConverter):
    def __init__(self, url_map, allowedExt=[], disallowedExt=[]):
        BaseConverter.__init__(self, url_map)
        excl = '|'.join(disallowedExt)
        incl = '|'.join(allowedExt)
        self.regex = '[^/].*?(?!\.abc)'#.format(excl)#, incl)
        print self.regex

class DirectoryConverter(BaseConverter):
    def __init__(self, url_map):
        BaseConverter.__init__(self, url_map)
        self.regex = '[^/].*?/'
