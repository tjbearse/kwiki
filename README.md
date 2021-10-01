# Kwiki
Kwiki provides a web interface to render and edit local markdown files. It can also render html, view text tiles, and list directories. Kwiki is consumed as a docker container ([hub page](https://hub.docker.com/repository/docker/tjbearse/kwiki)).

### Getting the Start Script
Kwiki has a companion script to start the container quickly and properly.

Download it alone and make it executable,
```console
curl -o kwiki.sh https://raw.githubusercontent.com/tjbearse/kwiki/master/kwiki.sh && chmod +x kwiki.sh
```

Alternately, clone this repository.

### Running Kwiki
To run kwiki, execute the kwiki script in a folder that has markdown or passing the folder as an argument. The start up script binds to a port chosen by docker and will to open the page in the browser when started.

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
