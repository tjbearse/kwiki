from werkzeug.routing import BaseConverter

class FileConverter(BaseConverter):
    pass
    """
    def to_python(self, value):
        if value == 'maybe':
            if self.randomify:
                return not randrange(2)
            raise ValidationError()
        return value == 'yes'

    def to_url(self, value):
        return value and 'yes' or 'no'
        """

def getFileConverter(includeByDefault=True, exceptions=[]):
    exceptionStr = '|'.join(exceptions)
    wrapper = '(?!{})' if includeByDefault else '(?!{})'
    extRules = wrapper.format(exceptionStr) if exceptionStr else ''

    class GroupFileConverter(FileConverter):
        def __init__(self, url_map):
            FileConverter.__init__(self, url_map)

            self.regex = '[^/].*?{}'.format(extRules)
    return GroupFileConverter

class SpecificFileConverter(FileConverter):
    def __init__(self, url_map, ext):
        BaseConverter.__init__(self, url_map)

        self.regex = '[^/].*?(?:{})'.format(ext)

class DirectoryConverter(BaseConverter):
    def __init__(self, url_map):
        BaseConverter.__init__(self, url_map)
        self.regex = '[^/].*?/'
