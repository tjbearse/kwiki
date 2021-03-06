#/bin/bash
set -ue

scriptPath=$(dirname "$0")
docker inspect kwiki >/dev/null 2>/dev/null || (cd "$scriptPath" && docker build -t kwiki .)

if [ $# -eq 0 ]
then
	path=$(pwd)
else
	path=$(realpath "$1")
fi
docker run --rm --publish 5000:5000 --mount "type=bind,src=${path},target=/home/files" kwiki
