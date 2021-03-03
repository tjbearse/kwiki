import subprocess
import flask
import os
import json

import converter

def search(in_str, root):
    escaped = in_str.translate({'"': r'\"'})
    args=('rg', '-i', '--json', '{}'.format(escaped))
    s = subprocess.run(args, cwd=root, capture_output=True).stdout.decode()

    ret = []
    for s in s.splitlines():
        j = json.loads(s)
        if j["type"] == "match":
            matchInfo = j["data"]
            name = matchInfo["path"]["text"]
            text = matchInfo["lines"]["text"]
            ret.append({
                'filename': os.path.basename(name),
                'path': os.path.split(name)[0],
                'link': flask.safe_join('/wiki/', name),
                'matchtext': flask.Markup(
                        converter.txt2html(text)
                )
            })
    return ret
