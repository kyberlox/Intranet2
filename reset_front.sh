#!/bin/sh

docker-compose down
git pull origin dev
docker images
docker rmi intranet_frontend
docker-compose up --build -d