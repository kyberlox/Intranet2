#!/bin/sh

docker-compose down
git pull origin dev
docker images
docker rmi intranet2-frontend
docker-compose up --build -d