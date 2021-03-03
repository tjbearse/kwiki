from python:3-alpine
workdir /home
RUN apk --no-cache add curl ripgrep npm
copy requirements.txt package.json package-lock.json copyStatic.sh ./
run npm install && ./copyStatic.sh && rm -rf node_modules
run pip install -r requirements.txt
copy . .
expose 5000
cmd ["python", "server.py", "files"]
