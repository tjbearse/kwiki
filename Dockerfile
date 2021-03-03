from python:3-alpine
workdir /home
RUN apk --no-cache add curl ripgrep
copy . .
run pip install -r requirements.txt
expose 5000
cmd ["python", "server.py", "files"]
