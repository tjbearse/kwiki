from python:2.7-alpine3.7
workdir /home
RUN apk --no-cache add curl
copy . .
run pip install -r requirements.txt
expose 5000
cmd ["python", "server.py", "files"]
