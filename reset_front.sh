#!/bin/sh

git pull origin main
docker-compose stop frontend
docker rmi intranet_frontend
docker-compose up -d frontend