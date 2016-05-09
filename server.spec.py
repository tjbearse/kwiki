import flask
import markdown
import os
import server
import tempfile
import unittest


import contextlib 

@contextlib.contextmanager
def monkey_patch(module, fn_name, patch):
    unpatch = getattr(module, fn_name)
    setattr(module, fn_name, patch)
    try:
        yield
    finally:
        setattr(module, fn_name, unpatch)

def setup_with_context_manager(testcase, cm):
    """Use a contextmanager to setUp a test case."""
    val = cm.__enter__()
    testcase.addCleanup(cm.__exit__, None, None, None)
    return val

def truth(*args):
    return True
def untrue(*args):
    return False


class MarkDownTests(unittest.TestCase):
    def setUp(self):
        server.app.config['TESTING'] = True
        server.app.config['root'] = '/start/'
        setup_with_context_manager(self, monkey_patch(os.path, 'isfile', truth))
        setup_with_context_manager(self, monkey_patch(flask, 'render_template', lambda *a, **k: k['content']))
        self.app = server.app.test_client()

    def tearDown(self):
        pass

    def test_returnsMarkdown(self):
        md = 'this is the markdown'
        with monkey_patch(markdown, 'markdownFromFile', lambda **k: k['output'].write(md)):
            r = self.app.get('/wiki.md')
            print 'r', r.get_data()
            self.assertEqual(r.data, flask.Markup(md))

    def test_usesFullPath(self):
        with monkey_patch(markdown, 'markdownFromFile', lambda **k : k['output'].write(k['input'])):
            r = self.app.get('/stuff/wiki.md')
            self.assertEqual(r.data, '/start/stuff/wiki.md')


    #fileDispatch
        # full path building
        # md files -> md
            # no ext case
        # non md files -> nonmd
        # dir -> dir
    #notMarkdown
        # don't test if fileDispatch is well tested
    #markdownFile
        # converts file
        # renders content into "content" slot of document.html template
    #listing
        # sep files vs dirs vs pages
        # filter .stuff
    # crumbs

if __name__ == '__main__':
    unittest.main()
