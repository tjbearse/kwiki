#/bin/sh

set -ue
mkdir -p static/media/fonts
cp node_modules/bootstrap/dist/fonts/* static/media/fonts/
cp node_modules/bootstrap/dist/css/bootstrap.min.css static/media/css/
cp node_modules/bootstrap/dist/js/bootstrap.min.js node_modules/jquery/dist/jquery.min.js static/media/js/
