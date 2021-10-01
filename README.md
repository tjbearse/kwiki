# Kwiki
Kwiki provides a web interface to render and edit local markdown files. It can also render html, view text tiles, and list directories. To start kwiki, run the start script in a folder that has markdown `cd markdown/; /path/to/kwiki.sh` or by passing a folder as an argument `/path/to/kwiki.sh ./markdown`. Kwik starts on localhost:5000.

## Usage Notes
- Kwiki starts a development server meant to be used from your local computer. It is not meant for public or production access.
- Currently Kwiki opens and writes all files as utf-8 encoding. This may change in the future.
- When a directory with an index file is opened, the index file will be rendered instead. Clicking the directory button will force open directory listing view.

## Features
- Directory listing and navigation
- Text file editing with preview render
- File search
- Markdown is enhanced with Jinja2 templating language. [Jinja2 template documentation](https://jinja2docs.readthedocs.io/en/stable/templates.html) 
- Markdown checklists (visual styling only, not interactable)
- Markdown TOC support
