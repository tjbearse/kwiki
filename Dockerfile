from python:3-alpine
workdir /home
RUN apk --no-cache add curl ripgrep npm
copy requirements.txt package.json package-lock.json ./

# install web assets and move them to static folder
run npm install && mkdir -p static/media/fonts static/media/css static/media/js && cp node_modules/bootstrap/dist/fonts/* static/media/fonts/ && cp node_modules/bootstrap/dist/css/bootstrap.min.css static/media/css/ && cp node_modules/bootstrap/dist/js/bootstrap.min.js node_modules/jquery/dist/jquery.min.js static/media/js/ && rm -rf node_modules

run pip install -r requirements.txt
copy . .
expose 5000
cmd ["python", "server.py", "files"]
