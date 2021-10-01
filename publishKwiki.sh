#/bin/bash
# builds and publishes kiwi to docker hub
set -ue

scriptPath=$(dirname "$0")
(cd "$scriptPath" && docker build -t tjbearse/kwiki . && docker push tjbearse/kwiki)
