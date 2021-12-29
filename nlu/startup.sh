# bin/bash

docker run -it -p 5005:5005 --mount "type=bind,source=$(pwd)/,target=/app" rasaimg
