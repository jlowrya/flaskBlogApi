 #!/bin/bash

docker build . -t blog-api
docker run --rm -p5100:5100 --name blog-api --cpus=1.0 blog-api:latest
