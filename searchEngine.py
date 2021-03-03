import subprocess
import flask
import os

import converter

def search(in_str):
    escaped = in_str.translate({'"': r'\"'})
    out = subprocess.getoutput('Ag -ila "{}"'.format(escaped)).splitlines()
    out.reverse()
    ret = [{
            'filename': os.path.basename(name),
            'path': os.path.split(name)[0],
            'link': flask.safe_join('/wiki/', name),
            'matchtext': flask.Markup(
                    converter.txt2html(
                        subprocess.getoutput(
                            'Ag -iC --nofilename "{}" {}'.format(in_str, name)
                        )
                    )
                )
        } for name in out]
    print('ret', ret)
    return ret
