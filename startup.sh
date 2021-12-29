# bin/bash

docker run -it -p 9000:9000 --mount "type=bind,source=$(pwd)/,target=/app" $1
