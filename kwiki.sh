#/bin/bash
# runs a kwiki container with the cwd or file argument mounted.
set -ue

print_usage() {
	printf "usage: $0 [-h] [path]"
}
print_help() {
	echo "runs a kwiki container with the cwd or file argument mounted."
	print_usage
}

while getopts 'h' flag; do
	case "${flag}" in
		h)
			print_help
			exit ;;
		*) print_usage
		   exit 1 ;;
	esac
done

if [ $# -eq 0 ]
then
	path=$(pwd)
else
	path=$(realpath "$1")
fi
container=$(docker run -d --rm -P --mount "type=bind,src=${path},target=/home/wiki" tjbearse/kwiki)
address=$(docker port "$container" 5000 | head -1)
address="http://${address}"
echo -e "\nExposed as $address on the local machine\n"
python -m webbrowser "$address" || true
docker logs -f "$container" || docker kill "$container" >/dev/null
