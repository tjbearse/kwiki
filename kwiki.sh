#/bin/bash
# runs a kwiki container with the cwd or file argument mounted.
set -ue

if [ $# -eq 0 ]
then
	path=$(pwd)
else
	path=$(realpath "$1")
fi
container=$(docker run -d --rm -P --mount "type=bind,src=${path},target=/home/files" tjbearse/kwiki)
address=$(docker port "$container" 5000 | head -1)
address="http://${address}"
echo -e "\nExposed as $address on the local machine\n"
python -m webbrowser "$address" || true
docker logs -f "$container"
